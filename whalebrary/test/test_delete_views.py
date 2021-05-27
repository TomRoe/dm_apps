from django.urls import reverse_lazy
from django.test import tag

from shared_models.views import CommonDeleteView, CommonPopoutDeleteView
from .. import models
from .. import views
from whalebrary import views
from whalebrary.test import FactoryFloor
from whalebrary.test.common_tests import CommonWhalebraryTest as CommonTest


# Example how to run with keyword tags
# python manage.py test whalebrary.test --tag transaction_new


class TestItemDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ItemFactory()
        self.test_url = reverse_lazy('whalebrary:item_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Item", "item_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ItemDeleteView, CommonDeleteView)
        self.assert_inheritance(views.ItemDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("Item", "item_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Item", "item_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.ItemFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Item.objects.filter(pk=self.instance.pk).count(), 0)


class TestLocationDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.LocationFactory()
        self.test_url = reverse_lazy('whalebrary:location_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Location", "location_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.LocationDeleteView, CommonDeleteView)
        self.assert_inheritance(views.LocationDeleteView, views.WhalebraryAdminAccessRequired)

    @tag("Location", "location_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Location", "location_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.LocationFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Location.objects.filter(pk=self.instance.pk).count(), 0)


class TestTransactionDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()
        self.test_url = reverse_lazy('whalebrary:transaction_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Transaction", "transaction_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransactionDeleteView, CommonDeleteView)
        self.assert_inheritance(views.TransactionDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("Transaction", "transaction_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Transaction", "transaction_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.TransactionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Transaction.objects.filter(pk=self.instance.pk).count(), 0)


class TestTransactionDeletePopoutView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()
        self.test_url = reverse_lazy('whalebrary:transaction_delete', kwargs={"pk": 1, "pop": 1})
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("TransactionDelete", "transaction_delete_pop", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransactionDeletePopoutView, CommonPopoutDeleteView)
        self.assert_inheritance(views.TransactionDeletePopoutView, views.WhalebraryEditRequiredMixin)

    @tag("TransactionDelete", "transaction_delete_pop", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("TransactionDelete", "transaction_delete_pop", "submit")
    def test_submit(self):
        data = FactoryFloor.TransactionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Transaction.objects.filter(pk=self.instance.pk).count(), 0)


class TestBulkTransactionDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()
        self.test_url = reverse_lazy('whalebrary:bulk_transaction_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("BulkTransaction", "bulk_transaction_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.BulkTransactionDeleteView, CommonDeleteView)
        self.assert_inheritance(views.BulkTransactionDeleteView, views.WhalebraryAdminAccessRequired)

    @tag("BulkTransaction", "bulk_transaction_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("BulkTransaction", "bulk_transaction_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.TransactionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Transaction.objects.filter(pk=self.instance.pk).count(), 0)


class TestOrderDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrderFactory()
        self.test_url = reverse_lazy('whalebrary:order_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Order", "order_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrderDeleteView, CommonDeleteView)
        self.assert_inheritance(views.OrderDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("Order", "order_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Order", "order_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.OrderFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Order.objects.filter(pk=self.instance.pk).count(), 0)


class TestOrderDeletePopoutView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrderFactory()
        self.test_url = reverse_lazy('whalebrary:order_delete', kwargs={"pk": 1, "pop": 1})
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("OrderDelete", "order_delete_pop", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrderDeletePopoutView, CommonPopoutDeleteView)
        self.assert_inheritance(views.OrderDeletePopoutView, views.WhalebraryEditRequiredMixin)

    @tag("OrderDelete", "order_delete_pop", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("OrderDelete", "order_delete_pop", "submit")
    def test_submit(self):
        data = FactoryFloor.OrderFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Order.objects.filter(pk=self.instance.pk).count(), 0)


class TestPersonnelDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonnelFactory()
        self.test_url = reverse_lazy('whalebrary:personnel_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Personnel", "personnel_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonnelDeleteView, CommonDeleteView)
        self.assert_inheritance(views.PersonnelDeleteView, views.WhalebraryAdminAccessRequired)

    @tag("Personnel", "personnel_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Personnel", "personnel_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonnelFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Personnel.objects.filter(pk=self.instance.pk).count(), 0)


class TestSupplierDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SupplierFactory()
        self.test_url = reverse_lazy('whalebrary:supplier_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Supplier", "supplier_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SupplierDeleteView, CommonDeleteView)
        self.assert_inheritance(views.SupplierDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("Supplier", "supplier_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Supplier", "supplier_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.SupplierFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Supplier.objects.filter(pk=self.instance.pk).count(), 0)


class TestSupplierDeletePopoutView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SupplierFactory()
        self.test_url = reverse_lazy('whalebrary:supplier_delete', kwargs={"pk": 1, "pop": 1})
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("SupplierDelete", "supplier_delete_pop", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SupplierDeletePopoutView, CommonPopoutDeleteView)
        self.assert_inheritance(views.SupplierDeletePopoutView, views.WhalebraryEditRequiredMixin)

    @tag("SupplierDelete", "supplier_delete_pop", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("SupplierDelete", "supplier_delete_pop", "submit")
    def test_submit(self):
        data = FactoryFloor.SupplierFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Supplier.objects.filter(pk=self.instance.pk).count(), 0)


class TestFileDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FileFactory()
        self.test_url = reverse_lazy('whalebrary:file_delete', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("File", "file_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FileDeleteView, CommonPopoutDeleteView)
        self.assert_inheritance(views.FileDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("File", "file_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("File", "file_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.FileFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.File.objects.filter(pk=self.instance.pk).count(), 0)


class TestIncidentDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IncidentFactory()
        self.test_url = reverse_lazy('whalebrary:incident_delete', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Incident", "incident_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.IncidentDeleteView, CommonDeleteView)
        self.assert_inheritance(views.IncidentDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("Incident", "incident_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Incident", "incident_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.IncidentFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Incident.objects.filter(pk=self.instance.pk).count(), 0)


class TestResightDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResightFactory()
        self.test_url = reverse_lazy('whalebrary:resight_delete', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Resight", "resight_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResightDeleteView, CommonPopoutDeleteView)
        self.assert_inheritance(views.ResightDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("Resight", "resight_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Resight", "resight_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.ResightFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Resight.objects.filter(pk=self.instance.pk).count(), 0)

    @tag("Resight", "resight_delete", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("whalebrary:resight_delete", f"/en/whalebrary/resight/{self.instance.pk}/delete/", [self.instance.pk])


class TestImageDeleteView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ImageFactory()
        self.test_url = reverse_lazy('whalebrary:image_delete', args=[self.instance.pk, ])
        self.expected_template = 'shared_models/generic_popout_confirm_delete.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Image", "image_delete", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ImageDeleteView, CommonDeleteView)
        self.assert_inheritance(views.ImageDeleteView, views.WhalebraryEditRequiredMixin)

    @tag("Image", "image_delete", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Image", "image_delete", "submit")
    def test_submit(self):
        data = FactoryFloor.ImageFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

        # for delete views...
        self.assertEqual(models.Image.objects.filter(pk=self.instance.pk).count(), 0)
