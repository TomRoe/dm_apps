from datetime import datetime

from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_models.api.serializers import PersonSerializer
from shared_models.api.views import _get_labels
from shared_models.models import Person, Language
from . import serializers
from .permissions import CanModifyRequestOrReadOnly, CanModifyProcessOrReadOnly
from .. import models, emails, model_choices, utils


# USER
#######
class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserDisplaySerializer(instance=request.user)
        data = serializer.data
        qp = request.GET
        if qp.get("request"):
            data["can_modify"] = utils.can_modify_request(request.user, qp.get("request"), return_as_dict=True)
        return Response(data)


class CSASRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CSASRequestSerializer
    permission_classes = [CanModifyRequestOrReadOnly]
    queryset = models.CSASRequest.objects.all()


class CSASRequestReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CSASRequestReviewSerializer
    permission_classes = [CanModifyRequestOrReadOnly]
    queryset = models.CSASRequestReview.objects.all()


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = models.Meeting.objects.all().order_by("-created_at")
    serializer_class = serializers.MeetingSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("process"):
            process = get_object_or_404(models.Process, pk=qp.get("process"))
            qs = process.meetings.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a csas process"))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MeetingNoteViewSet(viewsets.ModelViewSet):
    queryset = models.MeetingNote.objects.all()
    serializer_class = serializers.MeetingNoteSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("meeting"):
            meeting = get_object_or_404(models.Meeting, pk=qp.get("meeting"))
            qs = meeting.notes.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a meeting"))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MeetingCostViewSet(viewsets.ModelViewSet):
    queryset = models.MeetingCost.objects.all()
    serializer_class = serializers.MeetingCostSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("meeting"):
            meeting = get_object_or_404(models.Meeting, pk=qp.get("meeting"))
            qs = meeting.costs.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a meeting"))

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class InviteeViewSet(viewsets.ModelViewSet):
    queryset = models.Invitee.objects.all()
    serializer_class = serializers.InviteeSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    # pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        obj = serializer.save(updated_by=self.request.user)

        # it is important to use the try/except approach because this way
        # it can differentiate between  1) no dates value being passed or 2) a null value (i.e. clear all attendance)
        try:
            dates = self.request.data["dates"]
        except KeyError:
            pass
        else:
            # delete any existing attendance
            obj.attendance.all().delete()
            for date in dates.split(", "):
                dt = datetime.strptime(date.strip(), "%Y-%m-%d")
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
                models.Attendance.objects.create(invitee=obj, date=dt)

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("meeting"):
            meeting = get_object_or_404(models.Meeting, pk=qp.get("meeting"))
            qs = meeting.invitees.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a meeting"))


class MeetingResourceViewSet(viewsets.ModelViewSet):
    queryset = models.MeetingResource.objects.all()
    serializer_class = serializers.MeetingResourceSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    # pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        resource = serializer.save(created_by=self.request.user)

        # decide on who should receive an update
        for invitee in resource.meeting.invitees.all():
            # only send the email to those who already received an invitation (and where this happened in the past... redundant? )
            if invitee.invitation_sent_date and invitee.invitation_sent_date < resource.created_at:
                email = emails.NewResourceEmail(self.request, invitee, resource)
                email.send()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("meeting"):
            meeting = get_object_or_404(models.Meeting, pk=qp.get("meeting"))
            qs = meeting.resources.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a meeting"))


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("process"):
            process = get_object_or_404(models.Process, pk=qp.get("process"))
            qs = process.documents.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a csas process"))

    def post(self, request, pk):
        qp = request.query_params
        doc = get_object_or_404(models.Document, pk=pk)
        if qp.get("meeting"):
            meeting = get_object_or_404(models.Meeting, pk=qp.get("meeting"))
            if doc.meetings.filter(id=meeting.id).exists():
                doc.meetings.remove(meeting)
            else:
                doc.meetings.add(meeting)
            return Response(None, status.HTTP_204_NO_CONTENT)
        raise ValidationError(_("This endpoint cannot be used without a query param"))


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("document"):
            document = get_object_or_404(models.Document, pk=qp.get("document"))
            qs = document.authors.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a document"))

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class DocumentNoteViewSet(viewsets.ModelViewSet):
    queryset = models.DocumentNote.objects.all()
    serializer_class = serializers.DocumentNoteSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("document"):
            document = get_object_or_404(models.Document, pk=qp.get("document"))
            qs = document.notes.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a document"))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DocumentCostViewSet(viewsets.ModelViewSet):
    queryset = models.DocumentCost.objects.all()
    serializer_class = serializers.DocumentCostSerializer
    permission_classes = [CanModifyProcessOrReadOnly]

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        if qp.get("document"):
            document = get_object_or_404(models.Document, pk=qp.get("document"))
            qs = document.costs.all()
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
        raise ValidationError(_("You need to specify a document"))

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]


# this can probably be combined into the Invitee viewset
class InviteeSendInvitationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """ send the email"""
        invitee = get_object_or_404(models.Invitee, pk=pk)
        if not invitee.invitation_sent_date:
            # send email
            email = emails.InvitationEmail(request, invitee)
            email.send()
            invitee.invitation_sent_date = timezone.now()
            invitee.save()

            return Response("email sent.", status=status.HTTP_200_OK)
        return Response("An email has already been sent to this invitee.", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        """ get a preview of the email to be sent"""
        invitee = get_object_or_404(models.Invitee, pk=pk)
        # send email
        email = emails.InvitationEmail(request, invitee)
        return Response(email.as_dict(), status=status.HTTP_200_OK)


class MeetingModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Meeting

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        return Response(data)


class GenericNoteModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.GenericNote

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        data['type_choices'] = [dict(text=c[1], value=c[0]) for c in model_choices.note_type_choices]
        return Response(data)


class InviteeModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Invitee

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        data['person_choices'] = [dict(text=str(p), value=p.id) for p in Person.objects.all()]
        data['status_choices'] = [dict(text=c[1], value=c[0]) for c in model_choices.invitee_status_choices]
        data['role_choices'] = [dict(text=c[1], value=c[0]) for c in model_choices.invitee_role_choices]
        return Response(data)


class PersonModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = Person

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        data['language_choices'] = [dict(text=str(p), value=p.id) for p in Language.objects.all()]
        return Response(data)


class ResourceModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.MeetingResource

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        return Response(data)


class DocumentModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Document

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        return Response(data)


class AuthorModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Author

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        data['person_choices'] = [dict(text=str(p), value=p.id) for p in Person.objects.all()]
        return Response(data)


class GenericCostModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.GenericCost

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        data['cost_category_choices'] = [dict(text=c[1], value=c[0]) for c in model_choices.cost_category_choices]
        return Response(data)


class RequestModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.CSASRequest

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)
        return Response(data)


class RequestReviewModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.CSASRequestReview

    def get(self, request):
        data = dict()
        data['labels'] = _get_labels(self.model)

        prioritization_choices = [dict(text=c[1], value=c[0]) for c in model_choices.prioritization_choices]
        decision_choices = [dict(text=c[1], value=c[0]) for c in model_choices.request_decision_choices]
        prioritization_choices.insert(0, dict(text="-----", value=None))
        decision_choices.insert(0, dict(text="-----", value=None))
        data['prioritization_choices'] = prioritization_choices
        data['decision_choices'] = decision_choices
        return Response(data)
