from django import forms
from .models import EventTemplate

class EventTemplateForm(forms.ModelForm):
    """
    Form for creating/updating EventTemplate in Django admin.
    Enforces required fields and basic validation.
    """

    class Meta:
        model = EventTemplate
        fields = [
            "name",
            "day_of_week",
            "start_time",
            "end_time",
            "capacity",
            "start_date",
            "end_date",
        ]

    def clean_capacity(self):
        """
        Ensure capacity is positive.
        """
        capacity = self.cleaned_data.get("capacity")
        if capacity <= 0:
            raise forms.ValidationError("Capacity must be greater than zero.")
        return capacity
