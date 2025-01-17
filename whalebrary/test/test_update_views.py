from django.utils import timezone
from django.utils.translation import activate
from django.urls import reverse_lazy
from django.test import tag
from django.views.generic import DetailView, UpdateView

from shared_models.views import CommonDetailView, CommonUpdateView, CommonPopoutUpdateView
from whalebrary.test import FactoryFloor
from whalebrary.test.common_tests import CommonWhalebraryTest as CommonTest
from .. import views
from .. import models


# Example how to run with keyword tags
# python manage.py test whalebrary.test --tag transaction_new


class TestItemUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ItemFactory()
        self.test_url = reverse_lazy('whalebrary:item_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Item", "item_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ItemUpdateView, CommonUpdateView)
        self.assert_inheritance(views.ItemUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("Item", "item_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Item", "item_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.ItemFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestLocationUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.LocationFactory()
        self.test_url = reverse_lazy('whalebrary:location_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Location", "location_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.LocationUpdateView, CommonUpdateView)
        self.assert_inheritance(views.LocationUpdateView, views.WhalebraryAdminAccessRequired)

    @tag("Location", "location_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Location", "location_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.LocationFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestTransactionUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()
        self.test_url = reverse_lazy('whalebrary:transaction_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Transaction", "transaction_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransactionUpdateView, CommonUpdateView)
        self.assert_inheritance(views.TransactionUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("Transaction", "transaction_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Transaction", "transaction_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.TransactionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


# TODO check that kwargs can be static -- change all to args
class TestOrderReceivedTransactionUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()
        self.test_url = reverse_lazy('whalebrary:transaction_edit',
                                     kwargs={"pk": self.instance.id, "pop": 1})
        self.expected_template = 'shared_models/generic_popout_form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("OrderReceivedTransaction", "transaction_order_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrderReceivedTransactionUpdateView, CommonPopoutUpdateView)
        self.assert_inheritance(views.OrderReceivedTransactionUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("OrderReceivedTransaction", "transaction_order_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("OrderReceivedTransaction", "transaction_order_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.TransactionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestOrderUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrderFactory()
        self.test_url = reverse_lazy('whalebrary:order_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Order", "order_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrderUpdateView, CommonUpdateView)
        self.assert_inheritance(views.OrderUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("Order", "order_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Order", "order_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.OrderFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestOrderUpdatePopoutView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrderFactory()
        self.test_url = reverse_lazy('whalebrary:order_edit', kwargs={"pk": 1, "pop": 1})
        self.expected_template = 'shared_models/generic_popout_form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("OrderUpdate", "order_edit_pop", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrderUpdatePopoutView, CommonPopoutUpdateView)
        self.assert_inheritance(views.OrderUpdatePopoutView, views.WhalebraryEditRequiredMixin)

    @tag("OrderUpdate", "order_edit_pop", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)

    @tag("OrderUpdate", "order_edit_pop", "submit")
    def test_submit(self):
        data = FactoryFloor.OrderFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestPersonnelUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonnelFactory()
        self.test_url = reverse_lazy('whalebrary:personnel_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Personnel", "personnel_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonnelUpdateView, CommonUpdateView)
        self.assert_inheritance(views.PersonnelUpdateView, views.WhalebraryAdminAccessRequired)

    @tag("Personnel", "personnel_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Personnel", "personnel_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonnelFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestSupplierUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SupplierFactory()
        self.test_url = reverse_lazy('whalebrary:supplier_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Supplier", "supplier_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SupplierUpdateView, CommonUpdateView)
        self.assert_inheritance(views.SupplierUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("Supplier", "supplier_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Supplier", "supplier_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.SupplierFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestSupplierUpdatePopoutView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SupplierFactory()
        self.test_url = reverse_lazy('whalebrary:supplier_edit', kwargs={"pk": 1, "pop": 1})
        self.expected_template = 'shared_models/generic_popout_form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("SupplierUpdate", "supplier_edit_pop", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SupplierUpdatePopoutView, CommonPopoutUpdateView)
        self.assert_inheritance(views.SupplierUpdatePopoutView, views.WhalebraryEditRequiredMixin)

    @tag("SupplierUpdate", "supplier_edit_pop", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("SupplierUpdate", "supplier_edit_pop", "submit")
    def test_submit(self):
        data = FactoryFloor.SupplierFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestFileUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FileFactory()
        self.test_url = reverse_lazy('whalebrary:file_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/file_form_popout.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("File", "file_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FileUpdateView, CommonUpdateView)
        self.assert_inheritance(views.FileUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("File", "file_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("File", "file_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.FileFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestIncidentUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IncidentFactory()
        self.test_url = reverse_lazy('whalebrary:incident_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Incident", "incident_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.IncidentUpdateView, CommonUpdateView)
        self.assert_inheritance(views.IncidentUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("Incident", "incident_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Incident", "incident_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.IncidentFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestResightUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResightFactory()
        self.test_url = reverse_lazy('whalebrary:resight_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Resight", "resight_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResightUpdateView, CommonUpdateView)
        self.assert_inheritance(views.ResightUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("Resight", "resight_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Resight", "resight_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.ResightFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Resight", "resight_edit", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("whalebrary:resight_edit", f"/en/whalebrary/resight/{self.instance.pk}/edit/", [self.instance.pk])


class TestImageUpdateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ImageFactory()
        self.test_url = reverse_lazy('whalebrary:image_edit', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/image_form_popout.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Image", "image_edit", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ImageUpdateView, CommonUpdateView)
        self.assert_inheritance(views.ImageUpdateView, views.WhalebraryEditRequiredMixin)

    @tag("Image", "image_edit", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Image", "image_edit", "submit")
    def test_submit(self):
        data = FactoryFloor.ImageFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
