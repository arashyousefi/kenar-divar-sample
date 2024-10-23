from typing import List
from urllib.parse import quote_plus

import requests
from django.conf import settings
from django.urls import reverse


class DivarClient:
    OAUTH_REDIRECT_URL_TEMPLATE = (
        "/oauth2/auth?response_type=code"
        "&client_id={client_id}"
        "&redirect_uri={redirect_uri}"
        "&scope={scopes}"
        "&state={state}"
    )
    SCOPES = "USER_POSTS_GET USER_POSTS_GET USER_ADDON_CREATE USER_POSTS_ADDON_CREATE" \
        " CONVERSATION_SEND_MESSAGE.9c19c900-cc81-4ef5-a627-e51e87a1dab6"

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
            # "x-debug-token": settings.DIVAR_DEBUG_TOKEN,
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
            # "x-debug-token": settings.DIVAR_DEBUG_TOKEN,
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
                            # "action": {q
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
        print(response.status_code, response.json())
        if response.status_code != 200:
            ok = False
        else:
            ok = True
        return ok, response.json()

    def request_set_credit_score_to_post_v2(self, user, score: int, auth_data, post_token: str):
        url = f"{settings.DIVAR_BASE_URL}/v2/open-platform/addons/post/{post_token}"
        headers = {
            "x-api-key": settings.DIVAR_API_KEY,
            "x-access-token": auth_data.access_token,
            # "x-debug-token": settings.DIVAR_DEBUG_TOKEN,
        }

        data = {
            "widgets": [
                {
                    "evaluation_row": {
                        "left": {
                            "text": "cheap",
                            "section_color": "SUCESS_PRIMARY"
                        },
                        "middle": {
                            "text": "fair",
                            "section_color": "WARNING_SECONDARY"
                        },
                        "right": {
                            "text": "expensive",
                            "section_color": "ERROR_PRIMARY"
                        },
                        "indicator_text": "evaluation",
                        "indicator_percentage": 50,
                        "icon_name": "WC"
                    }
                },
                {
                    "button_bar": {
                        "title": "server link",
                        "action": {
                            "open_server_link": {
                                "data": {
                                    "foo": "bar",
                                }
                            }
                        }
                    }
                },
                {
                    "button_bar": {
                        "title": "direct link",
                        "action": {
                            "open_direct_link": "https://star-bunny-formally.ngrok-free.app",
                        }
                    }
                },
            ],
            "notes": "test note",
            "semantic": {
            },
        }

        response = requests.post(url, headers=headers, json=data, timeout=5)
        print(response.status_code, response.json())
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
        demand_button = {
            "action": "DIRECT_LINK",
            "data": {
                "icon_name": "نام آیکون مورد نظر برای این دکمه",
                "direct_link": settings.SITE_URL + reverse("logic:new-rating", args=[chat.supplier_id]),
                "caption": "امتیازدهی به آگهی گذار",
            }
        }
        supplier_button = {
            "action": "DIRECT_LINK",
            "data": {
                "icon_name": "نام آیکون مورد نظر برای این دکمه",
                "direct_link": settings.SITE_URL + reverse("logic:new-rating", args=[chat.demand_id]),
                "caption": "امتیازدهی به خریدار",
            }
        }
        if chat.user_id == chat.supplier_id:
            sender_button = supplier_button
            receiver_button = demand_button
        else:
            sender_button = demand_button
            receiver_button = supplier_button

        data = {
            "user_id": chat.user_id,
            "post_token": chat.post_token,
            "peer_id": chat.peer_id,
            "type": "TEXT",
            "message": message,
            "sender_btn": sender_button,
            "receiver_btn": receiver_button,
        }
        response = requests.post(url, headers=headers, json=data, timeout=5)
        if response.status_code != 200:
            ok = False
        else:
            ok = True
        return ok, response.json()

    def request_conversation_send_message(self, conversation_id: str, message: str, token: str):
        url = f"{settings.DIVAR_BASE_URL}/v2/open-platform/conversations/{conversation_id}/messages"
        headers = {
            "x-api-key": settings.DIVAR_API_KEY,
            "x-access-token": token,
            # "x-debug-token": settings.DIVAR_DEBUG_TOKEN,
        }

        data = {
            "message": message,
            "type": "TEXT",
            "receiver_buttons": {
                "rows": [
                    {
                        "buttons": [
                            {
                                "action": {
                                    "open_direct_link": "https://star-bunny-formally.ngrok-free.app/foo/bar/receiver",
                                },
                                "caption": "receiver direct",
                            },
                            {
                                "action": {
                                    "open_server_link": {
                                        "data": {
                                            "receiver": "true",
                                            "baz": "tux",
                                        }
                                    },
                                },
                                "icon_name": "TOC",
                                "caption": "receiver server",
                            }

                        ]
                    }
                ]
            },
            "sender_buttons": {
                "rows": [
                    {
                        "buttons": [
                            {
                                "action": {
                                    "open_direct_link": "https://star-bunny-formally.ngrok-free.app/foo/bar/sender",
                                },
                                "caption": "sender direct",
                            },
                            {
                                "action": {
                                    "open_server_link": {
                                        "data": {
                                            "receiver": "false",
                                            "baz": "tux",
                                        }
                                    },
                                },
                                "icon_name": "TOC",
                                "caption": "sender server",
                            }

                        ]
                    },
                    {
                        "buttons": [
                            {
                                "action": {
                                    "open_direct_link": "https://star-bunny-formally.ngrok-free.app/foo/bar/sender",
                                },
                                "caption": "big sender button",
                            }
                        ]
                    }
                ]
            }
        }
        response = requests.post(url, headers=headers, json=data, timeout=5)
        if response.status_code != 200:
            print(response.status_code)
            ok = False
        else:
            ok = True
        return ok, response.json()
