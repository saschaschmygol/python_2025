import requests
from django.conf import settings

# from comm_project.settings import TELEGRAM_BOT_TOKEN
import jwt
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken


def send_telegram_message(chat_id, text):
    """Отправка сообщения через Telegram API"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        print(f"Telegram send error: {e}")


def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        access_token = request.session.get("access_token")
        if not access_token:
            return redirect("login")
        try:

            token = AccessToken(access_token)
            request.user_id = token["user_id"]
        except jwt.InvalidTokenError:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper
