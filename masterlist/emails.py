from django.template import loader

from_email = 'DoNotReply@iHub.com'
admin_email = 'david.fishman@dfo-mpo.gc.ca'
stacy_email = 'Stacy.Adeogba@dfo-mpo.gc.ca'


class NewEntryEmail:
    def __init__(self, object):
        self.subject = 'a new entry has been made in the iHub web app'
        self.message = self.load_html_template(object)
        self.from_email = from_email
        self.to_list = [stacy_email]

    def load_html_template(self, object):
        t = loader.get_template('ihub/email_new_entry.html')
        context = {'object': object}
        rendered = t.render(context)
        return rendered