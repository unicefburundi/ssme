from django import template
import datetime
from ssme_activities.models import ProfileUser

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    exist = user.groups.filter(name=group_name).exists()
    profile = ProfileUser.objects.get(user=user).level == group_name
    return exist and profile


def format_to_time(date):
    d = datetime.datetime.strptime(date, "%d/%m/%Y")
    return d


def not_in_cds_group(user):
    if user:
        return user.groups.filter(name="CDS").count() == 0
    return False


def not_in_bds_group(user):
    if user:
        return user.groups.filter(name="BDS").count() == 0
    return False


def not_in_bps_group(user):
    if user:
        return user.groups.filter(name="BPS").count() == 0
    return False


def not_in_central_group(user):
    if user:
        return user.groups.filter(name="CEN").count() == 0
    return False
