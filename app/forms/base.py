from django import forms

from .widgets import MonthYearWidget, MonthYearField


class BaseStartDateEndDateForm(forms.ModelForm):
    start_date = MonthYearField(widget=MonthYearWidget(format="%Y-%m"), required=True)
    end_date = MonthYearField(widget=MonthYearWidget(format="%Y-%m"), required=False)

    class Meta:
        abstract = True
