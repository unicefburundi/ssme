from controlcenter import Dashboard, widgets

from ssme_activities.models import ReportBeneficiary


class BeneficiaryItemList(widgets.ItemList):
    model = ReportBeneficiary
    list_display = ("pk", "reception_date")
    list_display_links = ["reception_date"]


class MyDashboard(Dashboard):
    widgets = (BeneficiaryItemList,)
