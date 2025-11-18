from django.contrib import admin
from django.urls import path
from comm_app.views import (
    operator_reply,
    ticket_assign,
    get_all_message_ticket,
    get_ticket_user,
    get_all_ticket_open,
    login,
    register,
    ticket_close,
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/operator/reply/", operator_reply, name="operator_reply"),
    path("api/operator/ticket_assign/", ticket_assign, name="ticket_assign"),
    path("api/operator/ticket_close/", ticket_close, name="ticket_close"),
    path("api/operator/message_ticket/", get_all_message_ticket, name="message_ticket"),
    path("api/operator/tickets_user/", get_ticket_user, name="tickets_user"),
    path("api/operator/open_ticket/", get_all_ticket_open, name="open_ticket"),
    path("api/auth/register/", register, name="register"),
    path("api/auth/login/", login, name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
