from django.urls import path

from apps.divar.views import RedirectFromDivarView, ConnectToDivarView, DivarActionsView, AddCreditScoreView, \
    AddCreditScoreToPostView, ChatInitSessionView, HomePageView, ChatLandingView, SendRandomMessageView

app_name = 'divar'
urlpatterns = [
    path("connect", ConnectToDivarView.as_view(), name="connect"),
    path("redirect", RedirectFromDivarView.as_view(), name="redirect"),
    path("actions", DivarActionsView.as_view(), name="actions"),
    path("add-credit-score", AddCreditScoreView.as_view(), name="add-credit-score"),
    path("add-credit-score-to-post", AddCreditScoreToPostView.as_view(), name="add-credit-score-to-post"),
    path("start-chat", ChatInitSessionView.as_view(), name="chat-start"),
    path("chat-landing/<uuid>", ChatLandingView.as_view(), name="chat-landing"),
    path("send-random-message/<chat_uuid>", SendRandomMessageView.as_view(), name="send-random-message"),
]
