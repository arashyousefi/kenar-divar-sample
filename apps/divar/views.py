import uuid
from sqlite3 import connect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, FormView

from apps.divar.client import DivarClient
from apps.divar.forms import AddCreditScoreForm
from apps.divar.models import TempAuthorizationData
from apps.logic.models import CreditScore


class HomePageView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "divar/homepage.html"


class ConnectToDivarView(LoginRequiredMixin, RedirectView):
    login_url = "/login/"
    template_name = "connect_to_divar.html"

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        data, created = TempAuthorizationData.objects.get_or_create(user=user)
        if not created:
            data.state = uuid.uuid4()
            data.save(update_fields=['state'])
        client = DivarClient()
        return client.generate_redirect_url(state=str(data.state))


class RedirectFromDivarView(TemplateView):
    template_name = "divar/redirect_from_divar.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        params = request.GET
        print(params)
        context["params"] = params

        code = params.get('code', None)
        if code is None:
            context["result"] = "No code provided"
            return self.render_to_response(context)

        state = params.get('state', None)
        temp_data = TempAuthorizationData.objects.filter(state=state).first()
        if temp_data is None:
            context["result"] = "No data found"
            return self.render_to_response(context)
        client = DivarClient()
        ok, res = client.request_get_access_token(code)
        print(ok, res)
        if not ok:
            context["result"] = "Invalid response from Divar" + str(res)
            return self.render_to_response(context)

        if (access_token := res['access_token']) is None:
            context["result"] = "No access token found"
            return self.render_to_response(context)

        temp_data.access_token = access_token
        temp_data.scope = res['scope']
        temp_data.save(update_fields=['access_token', 'scope'])
        return HttpResponseRedirect(reverse("divar:actions"))


class DivarActionsView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "divar/actions.html"


class AddCreditScoreView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "divar/add_credit_score.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = request.user
        score, created = CreditScore.objects.get_or_create(user=user)
        context["score"] = score.score
        auth_data = TempAuthorizationData.objects.filter(user=user).first()
        if auth_data is None:
            context["ok"] = False
            context["result"] = "No auth data found"
            return self.render_to_response(context)

        client = DivarClient()
        ok, response = client.request_set_credit_score(user, score.score, auth_data)
        context["ok"] = ok
        context["result"] = response
        return self.render_to_response(context)


class AddCreditScoreToPostView(LoginRequiredMixin, FormView):
    login_url = "/login/"
    template_name = "divar/add_credit_score_to_post.html"
    form_class = AddCreditScoreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        score, created = CreditScore.objects.get_or_create(user=user)
        context['score'] = score.score
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        post_token = data['post_token']

        user = self.request.user
        score, created = CreditScore.objects.get_or_create(user=user)
        auth_data = TempAuthorizationData.objects.filter(user=user).first()
        if auth_data is None:
            print("No auth data found")
            return
        client = DivarClient()
        ok, response = client.request_set_credit_score_to_post(user, score.score, auth_data, post_token)
        print(ok, response)
        messages.success(self.request, "Your credit score has been added.")
        return HttpResponseRedirect(reverse("divar:actions"))
