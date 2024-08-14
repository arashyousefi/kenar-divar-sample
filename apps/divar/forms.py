from django import forms


class AddCreditScoreForm(forms.Form):
    post_token = forms.CharField()
