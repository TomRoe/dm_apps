from textile import textile

from . import models

# def resave_all(projects = models.Project.objects.all()):
#     for p in projects:
#         for obj in models.OMCategory.objects.all():
#             if not models.OMCost.objects.filter(project=p, om_category=obj).count():
#                 new_item = models.OMCost.objects.create(project=p, om_category=obj)
#                 new_item.save()

def resave_all(projects = models.Project.objects.all()):
    for p in projects:
        p.save()


def compare_html():
    projects = models.Project.objects.all()

    for p in projects:
        if p.description:
            if not textile(p.description) == p.description_html:
                print("mismatch in project {}".format(p.id))
        if p.priorities:
            if not textile(p.priorities) == p.priorities_html:
                print("mismatch in project {}".format(p.id))
        if p.deliverables:
            if not textile(p.deliverables) == p.deliverables_html:
                print("mismatch in project {}".format(p.id))


def replace_html():
    projects = models.Project.objects.all()

    for p in projects:
        should_save = False
        if p.description:
            p.description = p.description_html
            should_save = True

        if p.priorities:
            p.priorities = p.priorities_html
            should_save = True

        if p.deliverables:
            p.deliverables = p.deliverables_html
            should_save = True

        if should_save:
            p.save()


def clean_project():
    projects = models.Project.objects.all()

    for p in projects:
        p.is_negotiable = None
        p.save()


def copy_over_project_codes():
    projects = models.Project.objects.filter(existing_project_code__isnull=False)

    for p in projects:
        p.existing_project_codes.add(p.extisting_project_code)


