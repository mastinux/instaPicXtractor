from django.shortcuts import render
from instaPicXtractor import keys


class Authentication:
    """
        Server-side (Explicit) flow

    """

    AUTHORIZATION_URL = "https://api.instagram.com/oauth/authorize/" \
                        "?client_id=" + keys.INSTAGRAM_CLIENT_ID + \
                        "&redirect_uri=" + keys.INSTAGRAM_REDIRECT_URI + \
                        "&response_type=code"

    def get_authorization_url(self):
        return self.AUTHORIZATION_URL
