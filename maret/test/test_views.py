from django.test import tag
from django.urls import reverse_lazy

from shared_models.test import common_tests

from shared_models import views as shared_views
from maret import views


@tag('all', 'view', 'index')
class TestIndexView(common_tests.CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('maret:index')
        self.expected_template = 'maret/index.html'
        self.user = self.get_and_login_user(in_group="maret_admin")

    @tag('url')
    def test_correct_url(self):
        # use the 'en' locale prefix to url
        self.assert_correct_url("maret:index", f"/en/maret/")

    @tag('access')
    def test_view_access(self):
        self.assert_good_response(self.test_url)
        admin_user = self.get_and_login_user(in_group="maret_admin")
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=admin_user)

        author_user = self.get_and_login_user(in_group="maret_author")
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=author_user)

        user_user = self.get_and_login_user(in_group="maret_user")
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=user_user)

    @tag('class')
    def test_view_class(self):
        self.assert_inheritance(views.IndexView, shared_views.CommonTemplateView)


@tag('all', 'view', 'entry_list')
class TestEntryListView(common_tests.CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('maret:entry_list')
        self.expected_template = 'maret/entry_list.html'
        self.user = self.get_and_login_user(in_group="maret_admin")

    @tag("view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryListView, shared_views.CommonFilterView)

    @tag("access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


@tag('all', 'view', 'org_list')
class TestOrganizationListView(common_tests.CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('maret:org_list')
        self.expected_template = 'maret/organization_list.html'
        self.user = self.get_and_login_user(in_group="maret_admin")

    @tag("view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryListView, shared_views.CommonFilterView)

    @tag("access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)


@tag('all', 'view', 'person_list')
class TestPersonListView(common_tests.CommonTest):
    def setUp(self):
        super().setUp()
        self.test_url = reverse_lazy('maret:person_list')
        self.expected_template = 'maret/person_list.html'
        self.user = self.get_and_login_user(in_group="maret_admin")

    @tag("view")
    def test_view_class(self):
        self.assert_inheritance(views.EntryListView, shared_views.CommonFilterView)

    @tag("access")
    def test_view(self):
        self.assert_good_response(self.test_url)
        self.assert_non_public_view(test_url=self.test_url, expected_template=self.expected_template, user=self.user)

    @tag("context")
    def test_context(self):
        context_vars = [
            "field_list",
        ]
        self.assert_presence_of_context_vars(self.test_url, context_vars, user=self.user)
