from django.urls import path

from apps.divar.views import RedirectFromDivarView, ConnectToDivarView, DivarActionsView, AddCreditScoreView, \
    AddCreditScoreToPostView

app_name = 'divar'
urlpatterns = [
    path("connect", ConnectToDivarView.as_view(), name="connect"),
    path("redirect", RedirectFromDivarView.as_view(), name="redirect"),
    path("actions", DivarActionsView.as_view(), name="actions"),
    path("add-credit-score", AddCreditScoreView.as_view(), name="add-credit-score"),
    path("add-credit-score-to-post", AddCreditScoreToPostView.as_view(), name="add-credit-score-to-post"),
]
