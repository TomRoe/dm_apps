from django.urls import reverse_lazy
from django.test import tag

from shared_models.views import CommonCreateView
from whalebrary import views
from whalebrary.test import FactoryFloor
from whalebrary.test.FactoryFloor import ItemFactory
from whalebrary.test.common_tests import CommonWhalebraryTest as CommonTest

# Example how to run with keyword tags
# python manage.py test whalebrary.test --tag transaction_new


class TestItemCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ItemFactory()
        self.test_url = reverse_lazy('whalebrary:item_new')
        self.expected_template = "whalebrary/form.html"
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Item", "item_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ItemCreateView, CommonCreateView)
        self.assert_inheritance(views.ItemCreateView, views.WhalebraryEditRequiredMixin)

    @tag("Item", "item_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Item", "item_new", "submit")
    def test_submit(self):
        data = FactoryFloor.ItemFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestLocationCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.LocationFactory()
        self.test_url = reverse_lazy('whalebrary:location_new')
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Location", "location_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.LocationCreateView, CommonCreateView)
        self.assert_inheritance(views.LocationCreateView, views.WhalebraryAdminAccessRequired)

    @tag("Location", "location_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Location", "location_new", "submit")
    def test_submit(self):
        data = FactoryFloor.LocationFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestTransactionCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.TransactionFactory()
        self.test_url = reverse_lazy('whalebrary:transaction_new')
        self.test_url2 = reverse_lazy('whalebrary:transaction_new', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.expected_template2 = 'shared_models/generic_popout_form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Transaction", "transaction_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.TransactionCreateView, CommonCreateView)
        self.assert_inheritance(views.TransactionCreateView, views.WhalebraryEditRequiredMixin)

    @tag("Transaction", "transaction_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_good_response(self.test_url2)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template2, user=self.user)

    @tag("Transaction", "transaction_new", "submit")
    def test_submit(self):
        data = FactoryFloor.TransactionFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
        self.assert_success_url(self.test_url2, data=data, user=self.user)


class TestOrderCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.OrderFactory()
        self.test_url = reverse_lazy('whalebrary:order_new')
        self.test_url2 = reverse_lazy('whalebrary:order_new', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.expected_template2 = 'shared_models/generic_popout_form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Order", "order_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.OrderCreateView, CommonCreateView)
        self.assert_inheritance(views.OrderCreateView, views.WhalebraryEditRequiredMixin)

    @tag("Order", "order_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_good_response(self.test_url2)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template2, user=self.user)

    @tag("Order", "order_new", "submit")
    def test_submit(self):
        data = FactoryFloor.OrderFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
        self.assert_success_url(self.test_url2, data=data, user=self.user)


class TestPersonnelCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.PersonnelFactory()
        self.test_url = reverse_lazy('whalebrary:personnel_new')
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")

    @tag("Personnel", "personnel_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.PersonnelCreateView, CommonCreateView)
        self.assert_inheritance(views.PersonnelCreateView, views.WhalebraryAdminAccessRequired)

    @tag("Personnel", "personnel_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Personnel", "personnel_new", "submit")
    def test_submit(self):
        data = FactoryFloor.PersonnelFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestSupplierCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.SupplierFactory()
        self.test_url = reverse_lazy('whalebrary:supplier_new')
        self.test_url2 = reverse_lazy('whalebrary:supplier_new', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.expected_template2 = 'shared_models/generic_popout_form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_admin")
        ItemFactory(item_name="test")

    @tag("Supplier", "supplier_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.SupplierCreateView, CommonCreateView)
        self.assert_inheritance(views.SupplierCreateView, views.WhalebraryEditRequiredMixin)

    @tag("Supplier", "supplier_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_good_response(self.test_url2)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)
        self.assert_non_public_view(test_url=self.test_url2, expected_template=self.expected_template2, user=self.user)

    @tag("Supplier", "supplier_new", "submit")
    def test_submit(self):
        data = FactoryFloor.SupplierFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)
        self.assert_success_url(self.test_url2, data=data, user=self.user)


class TestFileCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.FileFactory()
        self.test_url = reverse_lazy('whalebrary:file_new', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/file_form_popout.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("File", "file_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.FileCreateView, CommonCreateView)
        self.assert_inheritance(views.FileCreateView, views.WhalebraryEditRequiredMixin)

    @tag("File", "file_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("File", "file_new", "submit")
    def test_submit(self):
        data = FactoryFloor.FileFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user, file_field_name="file")


class TestIncidentCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.IncidentFactory()
        self.test_url = reverse_lazy('whalebrary:incident_new')
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Incident", "incident_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.IncidentCreateView, CommonCreateView)
        self.assert_inheritance(views.IncidentCreateView, views.WhalebraryEditRequiredMixin)

    @tag("Incident", "incident_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Incident", "incident_new", "submit")
    def test_submit(self):
        data = FactoryFloor.IncidentFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)


class TestResightCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ResightFactory()
        self.test_url = reverse_lazy('whalebrary:resight_new', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/form.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Resight", "resight_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ResightCreateView, CommonCreateView)
        self.assert_inheritance(views.ResightCreateView, views.WhalebraryEditRequiredMixin)

    @tag("Resight", "resight_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Resight", "resight_new", "submit")
    def test_submit(self):
        data = FactoryFloor.ResightFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user)

    @tag("Resight", "resight_new", "correct_url")
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("whalebrary:resight_new", f"/en/whalebrary/resight/{self.instance.pk}/new/", [self.instance.pk])


class TestImageCreateView(CommonTest):
    def setUp(self):
        super().setUp()
        self.instance = FactoryFloor.ImageFactory()
        self.test_url = reverse_lazy('whalebrary:image_new', args=[self.instance.pk, ])
        self.expected_template = 'whalebrary/image_form_popout.html'
        self.user = self.get_and_login_user(in_group="whalebrary_edit")

    @tag("Image", "image_new", "view")
    def test_view_class(self):
        self.assert_inheritance(views.ImageCreateView, CommonCreateView)
        self.assert_inheritance(views.ImageCreateView, views.WhalebraryEditRequiredMixin)

    @tag("Image", "image_new", "access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("Image", "image_new", "submit")
    def test_submit(self):
        data = FactoryFloor.ImageFactory.get_valid_data()
        self.assert_success_url(self.test_url, data=data, user=self.user, file_field_name="image")
