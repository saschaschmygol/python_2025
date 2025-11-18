from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    TicketCloseSerializer,
    TicketAssignSerializer,
    TicketMessagesSerializer,
    OperatorReplySerializer,
)

from .service import TicketService, OperatorService


@api_view(["POST"])
def operator_reply(request):
    """Принять сообщение от Operator и отправить пользователю"""

    serializer = OperatorReplySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ticket = serializer.validated_data["ticket_id"]
    text = serializer.validated_data["text"]
    user = request.user

    try:
        response = OperatorService.reply(ticket, text, user.id)
        return Response(response, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": "Внутренняя ошибка сервера"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def ticket_assign(request):
    """Назначение тикета"""
    serializer = TicketAssignSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    ticket_id = serializer.validated_data["ticket_id"]

    try:
        ticket = TicketService.ticket_assign(ticket_id, user.id)
        return JsonResponse(
            {"status": "ok", "ticket_id": ticket_id, "user_id": user.id}
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": "Внутренняя ошибка сервера"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def ticket_close(request):
    """Закрытие тикета"""
    serializer = TicketCloseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    ticket_id = serializer.validated_data["ticket_id"]

    try:
        ticket = TicketService.close_ticket(ticket_id)
        return JsonResponse(
            {"status": "ok", "ticket_id": ticket_id, "user_id": user.id}
        )

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": "Внутренняя ошибка сервера"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def get_all_message_ticket(request):
    """Получение всех сообщений к тикету"""

    serializer = TicketMessagesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ticket_id = serializer.validated_data["ticket_id"]

    try:
        message_data = TicketService.get_messages_for_ticket(ticket_id)
        return JsonResponse({"ticket_id": ticket_id, **message_data})

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": "Внутренняя ошибка сервера"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_ticket_user(request):
    """Получение тикетов, привязанных к user"""
    user = request.user
    try:
        tickets = TicketService.get_ticket_user(user.id)
        return JsonResponse(tickets, safe=False)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": "Внутренняя ошибка сервера"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_all_ticket_open(request):
    """Получение всех свободных тикетов"""

    try:
        tickets = TicketService.get_ticket_open()
        return JsonResponse(tickets, safe=False)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(
            {"error": "Внутренняя ошибка сервера"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    from django.contrib.auth import authenticate

    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )
