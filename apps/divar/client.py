from typing import List
from urllib.parse import quote_plus

import requests
from django.conf import settings


class DivarClient:
    OAUTH_REDIRECT_URL_TEMPLATE = (
        "/oauth2/auth?response_type=code"
        "&client_id={client_id}"
        "&redirect_uri={redirect_uri}"
        "&scope={scopes}"
        "&state={state}"
    )
    SCOPES = "USER_POSTS_GET USER_POSTS_GET USER_ADDON_CREATE"

    def __init__(self):
        pass

    def generate_redirect_url(
            self, state: str, dynamic_scopes: List[str] = None
    ):
        scopes = self.SCOPES
        if dynamic_scopes:
            scopes += " " + " ".join(dynamic_scopes)

        path = self.OAUTH_REDIRECT_URL_TEMPLATE.format(
            client_id=settings.DIVAR_CLIENT_ID,
            client_secret=settings.DIVAR_CLIENT_SECRET,
            redirect_uri=quote_plus(settings.DIVAR_REDIRECT_URL),
            scopes=quote_plus(scopes),
            state=state,
        )
        return f"{settings.DIVAR_BASE_URL}{path}"

    def request_get_access_token(self, code: str):
        url = f"{settings.DIVAR_BASE_URL}/oauth2/token"
        data = {
            "code": code,
            "client_id": settings.DIVAR_CLIENT_ID,
            "client_secret": settings.DIVAR_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": settings.DIVAR_REDIRECT_URL,
        }
        response = requests.post(url, data=data, timeout=5)
        if response.status_code != 200:
            ok = False
        else:
            ok = True
        return ok, response.json()

    def request_set_credit_score(self, user, score: int, auth_data):
        url = f"{settings.DIVAR_BASE_URL}/v1/open-platform/addons/user/{user.mobile_number}"
        headers = {
            "x-api-key": settings.DIVAR_API_KEY,
            "x-access-token": auth_data.access_token,
        }

        data = {
            "widgets": {
                "widget_list": [
                    {
                        "widget_type": "SCORE_ROW",
                        "data": {
                            "@type": "type.googleapis.com/widgets.ScoreRowData",
                            "title": "امتیاز اعتبار",
                            "percentage_score": score,
                            "score_color": "SUCCESS_PRIMARY",
                            "hasDivider": True,
                            "icon": {
                                "icon_name": "HISTORY",
                                "icon_color": "SUCCESS_PRIMARY"
                            },
                            # "action": {
                            # "type": "LOAD_WEB_VIEW_PAGE",
                            # "fallback_link": "https://google.com/",
                            # "payload": {
                            #     "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
                            #     "url": "https://google.com/"
                            # }
                            # }
                        }
                    }
                ]
            },
            "notes": "test note",
            "phone": user.mobile_number,
            "categories": [],
            "management_permalink": "https://same-domain.com/manage/id",
            # "ticket_uuid": "812d56e6-e44d-45e7-8932-f9acbd416999",
            # "verification_cost": 124000,
            "semantic": {
                # "national_id": "0023456789",
                # "full_name": "علی علوی",
                # "external_reference": "ref-id"
            },
            # "semantic_sensitives": ["national_id"]
        }

        response = requests.post(url, headers=headers, json=data, timeout=5)
        if response.status_code != 200:
            ok = False
        else:
            ok = True
        return ok, response.json()

    def request_set_credit_score_to_post(self, user, score: int, auth_data, post_token: str):
        url = f"{settings.DIVAR_BASE_URL}/v1/open-platform/add-ons/post/{post_token}"
        headers = {
            "x-api-key": settings.DIVAR_API_KEY,
            "x-access-token": auth_data.access_token,
        }

        data = {
            "widgets": {
                "widget_list": [
                    {
                        "widget_type": "SCORE_ROW",
                        "data": {
                            "@type": "type.googleapis.com/widgets.ScoreRowData",
                            "title": "امتیاز اعتبار",
                            "percentage_score": score,
                            "score_color": "SUCCESS_PRIMARY",
                            "hasDivider": True,
                            "icon": {
                                "icon_name": "HISTORY",
                                "icon_color": "SUCCESS_PRIMARY"
                            },
                            # "action": {
                            # "type": "LOAD_WEB_VIEW_PAGE",
                            # "fallback_link": "https://google.com/",
                            # "payload": {
                            #     "@type": "type.googleapis.com/widgets.LoadWebViewPagePayload",
                            #     "url": "https://google.com/"
                            # }
                            # }
                        }
                    }
                ]
            },
            "notes": "test note",
            "phone": user.mobile_number,
            "categories": [],
            "management_permalink": "https://same-domain.com/manage/id",
            # "ticket_uuid": "812d56e6-e44d-45e7-8932-f9acbd416999",
            # "verification_cost": 124000,
            "semantic": {
                # "national_id": "0023456789",
                # "full_name": "علی علوی",
                # "external_reference": "ref-id"
            },
            # "semantic_sensitives": ["national_id"]
        }

        response = requests.post(url, headers=headers, json=data, timeout=5)
        if response.status_code != 200:
            ok = False
        else:
            ok = True
        return ok, response.json()

    def request_send_message_in_chat(self, auth_data, chat, message: str):
        url = f"{settings.DIVAR_BASE_URL}/v2/open-platform/chat/conversation"
        headers = {
            "x-api-key": settings.DIVAR_API_KEY,
            "x-access-token": auth_data.access_token,
        }
        data = {
            "user_id": chat.user_id,
            "post_token": chat.post_token,
            "peer_id": chat.peer_id,
            "type": "TEXT",
            "message": message,
            # "sender_btn": {
            #     "action": "LINK",
            #     "data": {
            #         "icon_name": "نام آیکون مورد نظر برای این دکمه",
            #         "extra_data": {
            #             "your_custom_key": "اطلاعاتی که در ادامه هنگام کلیک روی دکمه نیاز داریم"
            #         },
            #         "caption": "متن دکمهٔ زیر پیام برای طرف فرستنده"
            #     }
            # },
            # "receiver_btn": {
            #     "action": "LINK",
            #     "data": {
            #         "icon_name": "نام آیکون مورد نظر برای این دکمه",
            #         "extra_data": {
            #             "your_custom_key": "اطلاعاتی که در ادامه هنگام کلیک روی دکمه نیاز داریم"
            #         },
            #         "caption": "متن دکمهٔ زیر پیام برای طرف گیرنده"
            #     }
            # }
        }
        print(headers)
        response = requests.post(url, headers=headers, json=data, timeout=5)
        if response.status_code != 200:
            ok = False
        else:
            ok = True
        return ok, response.json()
