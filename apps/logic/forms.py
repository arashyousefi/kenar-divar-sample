from django import forms

from apps.logic.models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ("score",)