import os

from django.db import models
from django.dispatch import receiver

from .models import ReferenceMaterial, File, Staff, ProjectYear, Review


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = File.objects.get(pk=instance.pk).file
    except File.DoesNotExist:
        return False

    try:
        new_file = instance.file
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except ValueError:
        return False


@receiver(models.signals.post_delete, sender=ReferenceMaterial)
def auto_delete_ReferenceMaterial_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=ReferenceMaterial)
def auto_delete_ReferenceMaterial_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = ReferenceMaterial.objects.get(pk=instance.pk).file
    except ReferenceMaterial.DoesNotExist:
        return False

    new_file = instance.file
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=Staff)
def save_project_on_staff_delete(sender, instance, **kwargs):
    instance.project_year.project.save()


@receiver(models.signals.post_save, sender=Staff)
def save_project_on_staff_creation(sender, instance, created, **kwargs):
    instance.project_year.project.save()


@receiver(models.signals.post_delete, sender=ProjectYear)
def save_project_on_py_delete(sender, instance, **kwargs):
    instance.project.save()


@receiver(models.signals.post_save, sender=ProjectYear)
def save_project_on_py_creation(sender, instance, created, **kwargs):
    instance.project.save()


@receiver(models.signals.post_delete, sender=Review)
def save_project_year_on_review_delete(sender, instance, **kwargs):
    if instance.project_year.status == 3:
        py = instance.project_year
        py.status = 2
        py.save()


@receiver(models.signals.post_save, sender=Review)
def save_project_year_on_review_creation(sender, instance, created, **kwargs):
    if instance.project_year.status == 2:
        py = instance.project_year
        py.status = 3
        py.save()
