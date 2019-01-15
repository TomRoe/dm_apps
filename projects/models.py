from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
import os
import uuid

# Choices for language
ENG = 1
FRE = 2
LANGUAGE_CHOICES = (
    (ENG, 'English'),
    (FRE, 'French'),
)


# Create your models here.

class BudgetCode(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} ({})".format(self.code, self.name)

    class Meta:
        ordering = ['code', ]


class Division(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Section(models.Model):
    name = models.CharField(max_length=255)
    section_head = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Program(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Project(models.Model):
    fiscal_year = models.CharField(max_length=50, default="2019-2020")

    # basic
    project_title = models.TextField(verbose_name="Project title")
    division = models.ForeignKey(Division, on_delete=models.DO_NOTHING, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="projects")
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING, blank=True, null=True)
    budget_code = models.ForeignKey(BudgetCode, on_delete=models.DO_NOTHING, related_name="is_section_head_on_projects",
                                    blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True,
                               verbose_name="project status")
    approved = models.BooleanField(default=False, verbose_name="Has this project already been approved?")
    start_date = models.DateTimeField(blank=True, null=True, verbose_name="Start Date")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="End Date")

    # details
    description = models.TextField(blank=True, null=True, verbose_name="Project Objective & Description")
    priorities = models.TextField(blank=True, null=True, verbose_name="Project-specific priorities in 2019/2020")
    deliverables = models.TextField(blank=True, null=True,
                                    verbose_name="Project Deliverables in 2019 / 2020 (bulleted form)")

    # data
    data_collection = models.TextField(blank=True, null=True, verbose_name="What type of data will be collected?")
    data_sharing = models.TextField(blank=True, null=True,
                                    verbose_name="Which of these data will be share-worthy and what is the plan to share / disseminate?")
    data_storage = models.TextField(blank=True, null=True, verbose_name="Data Storage / Archiving Plan")
    metadata_url = models.URLField(blank=True, null=True, verbose_name="please provide link to metadata, if available")

    # needs
    regional_dm = models.NullBooleanField(
        verbose_name="Does the program require assistance of the branch data manager?")
    regional_dm_needs = models.TextField(blank=True, null=True,
                                         verbose_name="If yes, please describe")
    sectional_dm = models.NullBooleanField(
        verbose_name="Does the program require assistance of the section's data manager?")
    sectional_dm_needs = models.TextField(blank=True, null=True,
                                          verbose_name="If yes, please describe")
    vehicle_needs = models.TextField(blank=True, null=True,
                                     verbose_name="Describe need for vehicle (type of vehicle, number of weeks, time-frame)")
    it_needs = models.TextField(blank=True, null=True, verbose_name="IT Requirements (software, licenses, hardware)")
    chemical_needs = models.TextField(blank=True, null=True,
                                      verbose_name="Please provide details regarding chemical needs and the plan for storage and disposal.")
    ship_needs = models.TextField(blank=True, null=True, verbose_name="Ship (Coast Guard, Charter) Requirements")

    # admin
    feedback = models.TextField(blank=True, null=True,
                                verbose_name="Do you have any feedback you would like to submit about this process?")
    submitted = models.BooleanField(default=False, verbose_name="Submit project for review")
    date_last_modified = models.DateTimeField(blank=True, null=True, default=timezone.now)
    last_modified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return "{}".format(self.project_title)

    def save(self, *args, **kwargs):
        self.date_last_modified = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.pk})


class EmployeeType(models.Model):
    # cost_type choices
    SAL = 1
    OM = 2
    COST_TYPE_CHOICES = [
        (SAL, "Salary"),
        (OM, "O&M"),
    ]

    name = models.CharField(max_length=255)
    cost_type = models.IntegerField(choices=COST_TYPE_CHOICES)

    def __str__(self):
        return "{}".format(self.name)


class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['name', ]


class Staff(models.Model):
    # STUDENT_PROGRAM_CHOICES
    FSWEP = 1
    COOP = 1
    STUDENT_PROGRAM_CHOICES = [
        (FSWEP, "FSWEP"),
        (COOP, "Coop"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="staff_members")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="User")
    name = models.CharField(max_length=255, verbose_name="Person name (leave blank if user is selected)", blank=True,
                            null=True)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.DO_NOTHING)
    level = models.ForeignKey(Level, on_delete=models.DO_NOTHING, blank=True, null=True)
    student_program = models.IntegerField(choices=STUDENT_PROGRAM_CHOICES, blank=True, null=True)
    duration_weeks = models.FloatField(default=0, blank=True, null=True)
    overtime_hours = models.FloatField(default=0, blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)

    def __str__(self):
        if self.user:
            return "{} {}".format(self.user.first_name, self.user.last_name)
        else:
            return "{}".format(self.name)

    class Meta:
        ordering = ['employee_type', 'level']


class Collaborator(models.Model):
    # TYPE_CHOICES
    COL = 1
    PAR = 2
    TYPE_CHOICES = [
        (COL, "Collaborator"),
        (PAR, "Partner"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="collaborators")
    name = models.CharField(max_length=255, verbose_name="Name", blank=True,
                            null=True)
    type = models.IntegerField(choices=TYPE_CHOICES)
    critical = models.BooleanField(default=True, verbose_name="Critical to project delivery")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return "{}".format(self.name)


class CollaborativeAgreement(models.Model):
    # NEW_OR_EXISTING_CHOICES
    NEW = 1
    EXIST = 2
    NEW_OR_EXISTING_CHOICES = [
        (NEW, "New"),
        (EXIST, "Existing"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="agreements")
    partner_organization = models.CharField(max_length=255, blank=True, null=True)
    project_lead = models.CharField(max_length=255, blank=True, null=True)
    agreement_title = models.CharField(max_length=255, verbose_name="Title of the agreement", blank=True, null=True)
    new_or_existing = models.IntegerField(choices=NEW_OR_EXISTING_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['partner_organization', ]

    def __str__(self):
        return "{}".format(self.partner_organization)


class OMCategory(models.Model):
    # group choices:
    TRAV = 1
    EQUIP = 2
    MAT = 3
    HR = 4
    OTH = 5
    GROUP_CHOICES = (
        (TRAV, "Travel"),
        (EQUIP, "Equipment Purchase"),
        (MAT, "Material and Supplies"),
        (HR, "Human Resources"),
        (OTH, "Contracts, Leases, Services"),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    group = models.IntegerField(choices=GROUP_CHOICES)

    class Meta:
        ordering = ['group', 'name']

    def __str__(self):
        return "{} ({})".format(self.name, self.get_group_display())


class OMCost(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="om_costs")
    om_category = models.ForeignKey(OMCategory, on_delete=models.DO_NOTHING, related_name="om_costs",
                                    verbose_name="category")
    description = models.TextField(blank=True, null=True)
    budget_requested = models.FloatField(default=0)

    def __str__(self):
        return "{}".format(self.om_category)

    class Meta:
        ordering = ['om_category', ]


class CapitalCost(models.Model):
    # category choices:
    IMIT = 1
    LAB = 2
    FIELD = 3
    OTH = 4
    CATEGORY_CHOICES = (
        (IMIT, "IM / IT - computers, hardware"),
        (LAB, "Lab Equipment"),
        (FIELD, "Field Equipment"),
        (OTH, "Other"),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="capital_costs")
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    budget_requested = models.FloatField(default=0)

    def __str__(self):
        return "{}".format(self.get_category_display())

    class Meta:
        ordering = ['category', ]


class GCCost(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gc_costs")
    recipient_org = models.CharField(max_length=255, blank=True, null=True, verbose_name="Recipient organization")
    project_lead = models.CharField(max_length=255, blank=True, null=True)
    proposed_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Proposed title of agreement")
    gc_program = models.CharField(max_length=255, blank=True, null=True, verbose_name="Name of G&C program")
    budget_requested = models.FloatField(default=0)

    def __str__(self):
        return "{} - {}".format(self.recipient_org, self.gc_program)

    class Meta:
        ordering = ['recipient_org', ]