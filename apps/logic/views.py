from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.views.generic import FormView

from apps.logic.forms import RatingForm
from apps.logic.models import Rating


class NewRatingView(FormView):
    template_name = "logic/rating.html"
    form_class = RatingForm
    def get_context_data(self, **kwargs):
        user_uuid = self.kwargs['user_uuid']
        return super().get_context_data(user_uuid=user_uuid, **kwargs)


    def form_valid(self, form):
        Rating.objects.create(user_uuid=self.kwargs['user_uuid'], score=form.cleaned_data['score'])
        return super().form_valid(form)

    def get_success_url(self):
        return "https://open-platform-redirect.divar.ir/completion" # todo
