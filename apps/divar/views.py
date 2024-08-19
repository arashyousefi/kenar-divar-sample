import random
import string
import uuid
from base64 import b64encode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, FormView, DetailView
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.divar.client import DivarClient
from apps.divar.forms import AddCreditScoreForm
from apps.divar.models import TempAuthorizationData, Chat, ChatMessage
from apps.divar.serializers import InitSessionFromChatSerializer
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

        required_scope = f"POST_ADDON_CREATE.{post_token}"
        client = DivarClient()

        auth_data = TempAuthorizationData.objects.filter(user=user, scope__contains=required_scope).first()
        if auth_data is None:
            auth_data = TempAuthorizationData.objects.create(user=user)
            return HttpResponseRedirect(client.generate_redirect_url(auth_data.state, dynamic_scopes=[required_scope]))

        ok, response = client.request_set_credit_score_to_post(user, score.score, auth_data, post_token)
        messages.success(self.request, "Your credit score has been added.")
        return HttpResponseRedirect(reverse("divar:actions"))


class ChatInitSessionView(APIView):
    def post(self, request, *args, **kwargs):
        auth_token = self.request.headers['Authorization']
        if auth_token != settings.DIVAR_IDENTIFICATION_KEY:
            raise exceptions.AuthenticationFailed()
        data = request.data
        serializer = InitSessionFromChatSerializer(data=data)
        if not serializer.is_valid():
            raise exceptions.ValidationError(serializer.errors)
        latitude = serializer.validated_data.get("location", {}).get("latitude", None)
        longitude = serializer.validated_data.get("location", {}).get("longitude", None)
        chat, _ = Chat.objects.get_or_create(
            post_token=serializer.validated_data.get("post_token"),
            user_id=serializer.validated_data.get("user_id", None),
            peer_id=serializer.validated_data.get("peer_id", None),
            defaults={
                "latitude": latitude,
                "longitude": longitude,
                "callback_url": serializer.validated_data.get("callback_url", None),
                "supplier_id": serializer.validated_data.get("supplier", {}).get("id", None),
                "demand_id": serializer.validated_data.get("demand", {}).get("id", None),
            }
        )
        response = {
            "status": "200",
            "message": "success",
            "url": settings.SITE_URL + reverse("divar:chat-landing", args=[chat.uuid]),
        }
        return Response(data=response, status=status.HTTP_200_OK)


class ChatLandingView(DetailView):
    template_name = "divar/chat_landing.html"
    context_object_name = "chat"

    def get_queryset(self):
        return Chat.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, uuid=self.kwargs['uuid'])


class SendRandomMessageView(TemplateView):
    def get(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, uuid=self.kwargs['chat_uuid'])
        client = DivarClient()
        scope_identifier = f"{chat.user_id}:{chat.post_token}:{chat.peer_id}"
        scope = f"CHAT_MESSAGE_SEND.{b64encode(scope_identifier.encode()).decode()}"
        if not (auth_data := TempAuthorizationData.objects.filter(user_uuid=chat.user_id, scope__contains=scope,
                                                                  access_token__isnull=False).first()):
            auth_data = TempAuthorizationData.objects.create(user_uuid=chat.user_id)
            return HttpResponseRedirect(client.generate_redirect_url(auth_data.state, dynamic_scopes=[scope]))

        message = "".join(random.choices(string.ascii_letters + string.digits, k=100))
        message = "به کاربر مقابل امتیاز بدهید\n" + message
        ok, response = client.request_send_message_in_chat(auth_data, chat, message)
        if ok:
            ChatMessage.objects.create(
                chat=chat,
                message_text=message,
            )
        return HttpResponseRedirect(reverse("divar:chat-landing", args=[chat.uuid]))
