from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView,  UpdateView, DeleteView, CreateView, DetailView
from django_filters.views import FilterView
import json
from . import models
from . import forms
from . import filters
from . import emails


# Create your views here.
class CloserTemplateView(TemplateView):
    template_name = 'dm_tickets/close_me.html'


# Ticket #
##########

class TicketListView(FilterView):
    # model = models.Ticket
    filterset_class = filters.TicketFilter
    template_name = "dm_tickets/ticket_list.html"

    # def get_filterset_kwargs(self, filterset_class):
    #     kwargs = super().get_filterset_kwargs(filterset_class)
    #     if kwargs["data"] is None:
    #         kwargs["data"] = {"status": 5}
    #     return kwargs

class TicketDetailView(DetailView):
    model = models.Ticket
    template_name = "dm_tickets/ticket_detail.html"
    # form_class = forms.TicketDetailForm

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)

        try:
            extra_context = {'temp_msg':self.request.session['temp_msg']}
            context.update(extra_context)
            del self.request.session['temp_msg']
        except Exception as e:
            print("type error: " + str(e))
            # pass
        context['email'] = emails.TicketResolvedEmail(self.object)

        return context

def send_resolved_email(request, ticket):
    # grab a copy of the resource
    my_ticket = models.Ticket.objects.get(pk=ticket)
    # create a new email object
    email = emails.TicketResolvedEmail(my_ticket)
    # send the email object
    if settings.MY_ENVR != 'dev':
        send_mail( message='', subject=email.subject, html_message=email.message, from_email=email.from_email, recipient_list=email.to_list,fail_silently=False,)
    else:
        print('not sending email since in dev mode')
    my_ticket.resolved_email_date = timezone.now()
    my_ticket.save()
    messages.success(request, "the email has been sent!")
    return HttpResponseRedirect(reverse('tickets:detail', kwargs={'pk':ticket}))



class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    template_name = "dm_tickets/ticket_form.html"
    login_url = '/accounts/login_required/'
    form_class = forms.TicketForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # produce a dictionary of people
        email_dict = {}
        for person in models.Person.objects.all():
            email_dict[person.id] = person.email
        # convert dict to JSON
        email_json = json.dumps(email_dict)
        # send JSON file to template so that it can be used by js script
        context['email_json'] = email_json
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.primary_contact.email = form.cleaned_data["primary_contact_email"]
        self.object.primary_contact.save()
        return HttpResponseRedirect(self.get_success_url())

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Ticket
    success_url = reverse_lazy('tickets:list')
    login_url = '/accounts/login_required/'

class TicketCreateView(CreateView):
    model = models.Ticket
    login_url = '/accounts/login_required/'
    form_class = forms.TicketForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # produce a dictionary of people
        email_dict = {}
        for person in models.Person.objects.all():
            email_dict[person.id] = person.email
        # convert dict to JSON
        email_json = json.dumps(email_dict)
        # send JSON file to template so that it can be used by js script
        context['email_json'] = email_json
        return context

    def form_valid(self, form):
        self.object = form.save()
        # do something with self.object #
        #################################
        self.object.people.add(self.object.primary_contact)
        # update the primary contact email with the form data
        self.object.primary_contact.email = form.cleaned_data["primary_contact_email"]
        self.object.primary_contact.save()

        # create a new email object
        email = emails.NewTicketEmail(self.object)
        # send the email object
        if settings.MY_ENVR != 'dev':
            send_mail( message='', subject=email.subject, html_message=email.message, from_email=email.from_email, recipient_list=email.to_list,fail_silently=False,)
        else:
            print('not sending email since in dev mode')

        messages.success(self.request, "The new ticket has been logged and a confirmation email has been sent!")
        return HttpResponseRedirect(self.get_success_url())

class TicketNoteUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Ticket
    template_name = "dm_tickets/ticket_note_form.html"
    login_url = '/accounts/login_required/'
    form_class = forms.TicketNoteForm


# Service Desk Ticket #
#######################

class ServiceDeskDetailView(UpdateView):
    model = models.ServiceDeskTicket
    form_class = forms.ServiceDeskTicketForm
    template_name ='dm_tickets/service_desk_ticket_detail_popout.html'

class ServiceDeskUpdateView(LoginRequiredMixin, UpdateView):
    model = models.ServiceDeskTicket
    form_class = forms.ServiceDeskTicketForm
    template_name ='dm_tickets/service_desk_ticket_form_popout.html'
    login_url = '/accounts/login_required/'

class ServiceDeskCreateView(LoginRequiredMixin, CreateView):
    model = models.ServiceDeskTicket
    form_class = forms.ServiceDeskTicketForm
    template_name ='dm_tickets/service_desk_ticket_form_popout.html'
    login_url = '/accounts/login_required/'

    def get_success_url(self, **kwargs):
        return reverse('tickets:close_me')


# Tags #
########

class TagDetailView(UpdateView):
    model = models.Tag
    template_name ='dm_tickets/tag_detail_popout.html'
    form_class = forms.TagForm

class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Tag
    template_name ='dm_tickets/tag_form_popout.html'
    login_url = '/accounts/login_required/'
    form_class = forms.TagForm

class TagCreateView(CreateView):
    model = models.Tag
    template_name ='dm_tickets/tag_form_popout.html'
    form_class = forms.TagForm

    def form_valid(self, form):
        self.object = form.save()
        ticket = self.kwargs['ticket']
        return HttpResponseRedirect(reverse_lazy('tickets:add_tag', kwargs={'ticket':ticket, 'tag':self.object.id}))

class TagListView(FilterView):
    filterset_class = filters.TagFilter
    template_name = "dm_tickets/tag_insert_list.html"

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        ticket = self.kwargs['ticket']
        context['ticket']= ticket
        return context

def add_tag_to_ticket(request, ticket, tag):
    my_ticket = models.Ticket.objects.get(id=ticket)
    my_ticket.tags.add(tag)
    return HttpResponseRedirect(reverse('tickets:tag_insert', kwargs={'ticket':ticket}))

# Files #
#########

class FileCreateView(CreateView):
    model = models.File
    fields = '__all__'
    template_name ='dm_tickets/file_form_popout.html'
    login_url = '/accounts/login_required/'
    # form_class = forms.StudentCreateForm

    def get_initial(self):
        ticket = models.Ticket.objects.get(pk=self.kwargs['ticket'])
        return {'ticket': ticket}

    def form_valid(self, form):
        self.object = form.save()

        # create a new email object
        email = emails.NewFileAddedEmail(self.object)
        # send the email object
        if settings.MY_ENVR != 'dev':
            send_mail( message='', subject=email.subject, html_message=email.message, from_email=email.from_email, recipient_list=email.to_list,fail_silently=False,)
        else:
            print('not sending email since in dev mode')

        #store a temporary message is the sessions middleware
        self.request.session['temp_msg'] = "The new file has been added and a notification email has been sent to the site administrator."

        return HttpResponseRedirect(self.get_success_url())

class FileUpdateView(UpdateView):
    model = models.File
    fields = '__all__'
    template_name ='dm_tickets/file_form_popout.html'
    # form_class = forms.StudentCreateForm

class FileDetailView(UpdateView):
    model = models.File
    fields = '__all__'
    template_name ='dm_tickets/file_detail_popout.html'
    # form_class = forms.TagForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            extra_context = {'temp_msg':self.request.session['temp_msg']}
            context.update(extra_context)
            del self.request.session['temp_msg']
        except Exception as e:
            print("type error: " + str(e))
            # pass

        return context

# People #
##########

class PersonDetailView(UpdateView):
    model = models.Person
    template_name ='dm_tickets/person_detail_popout.html'
    fields = '__all__'

class PersonUpdateView(UpdateView):
    model = models.Person
    template_name ='dm_tickets/person_form_popout.html'
    login_url = '/accounts/login_required/'
    fields = '__all__'

class PersonCreateView(CreateView):
    model = models.Person
    template_name ='dm_tickets/person_form_popout.html'
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        try:
            ticket = self.kwargs['ticket']
        except:
            return HttpResponseRedirect(reverse('tickets:close_me'))
        else:
            return HttpResponseRedirect(reverse_lazy('tickets:add_person', kwargs={'ticket':ticket, 'person':self.object.id}))




class PersonListView(FilterView):
    filterset_class = filters.PersonFilter
    template_name = "dm_tickets/person_insert_list.html"

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        ticket = self.kwargs['ticket']
        context['ticket']= ticket
        return context

def add_person_to_ticket(request, ticket, person):
    my_ticket = models.Ticket.objects.get(id=ticket)
    my_ticket.people.add(person)
    return HttpResponseRedirect(reverse('tickets:person_insert', kwargs={'ticket':ticket}))

# Request Type #
################


class RequestTypeCreateView(CreateView):
    model = models.RequestType
    template_name ='dm_tickets/request_type_form_popout.html'
    fields = '__all__'

    def get_success_url(self, **kwargs):
        return reverse('tickets:close_me')