# services.py (новый файл в app)
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Ticket, User, MessageIn, MessageOut
from .utils import send_telegram_message


class TicketService:
    @classmethod
    @transaction.atomic  # Атомарность: если ошибка — rollback
    def close_ticket(cls, ticket_id: int) -> Ticket:
        """
        Закрывает тикет для пользователя
        """
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if ticket.status == "closed":
                raise ValueError("Тикет уже закрыт")

            text = "Оператор закрыл ваше обращение"
            chat_id = ticket.chat.tg_chat_id
            send_telegram_message(chat_id, text)

            ticket.status = "closed"
            ticket.save(update_fields=["status"])

            return ticket

        except Ticket.DoesNotExist:
            raise ValueError(f"Тикет с ID {ticket_id} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка закрытия тикета: {str(e)}")

    @classmethod
    @transaction.atomic
    def ticket_assign(cls, ticket_id: int, user_id: int) -> Ticket:
        """
        Назначает тикет на оператора
        """
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            user = User.objects.get(id=user_id)

            ticket.status = "appointed"
            ticket.user = user
            ticket.save(update_fields=["status", "user"])

            return ticket  # Возвращаем для response

        except Ticket.DoesNotExist:
            raise ValueError(f"Тикет с ID {ticket_id} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка назначения тикета: {str(e)}")

    @classmethod
    def get_messages_for_ticket(cls, ticket_id: int) -> dict:
        """
        Получает все входящие и исходящие сообщения для тикета
        """
        try:
            messages_in = list(MessageIn.objects.filter(ticket_id=ticket_id).values())
            messages_out = list(MessageOut.objects.filter(ticket_id=ticket_id).values())

            return {
                "messages_in": messages_in,
                "messages_out": messages_out,
            }

        except ObjectDoesNotExist:
            raise ValueError(f"Тикет с ID {ticket_id} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка получения сообщений: {str(e)}")

    @classmethod
    def get_ticket_open(cls) -> list:
        """Получение всех открытых тикетов"""
        try:
            tickets = list(Ticket.objects.filter(status="open").values())

            return tickets

        except Exception as e:
            raise ValueError(f"Ошибка получения тикетов: {str(e)}")

    @classmethod
    def get_ticket_user(cls, user_id: int) -> list:
        """Получение всех тикетов user"""
        try:
            tickets = list(Ticket.objects.filter(user_id=user_id).values())

            return tickets

        except Exception as e:
            raise ValueError(f"Ошибка получения тикетов: {str(e)}")


class OperatorService:
    @classmethod
    @transaction.atomic  # Атомарность: если ошибка — rollback
    def reply(cls, ticket: Ticket, text: str, user_id: int) -> dict:
        """
        Отправка ответа от оператора.
        """
        try:
            user = User.objects.get(id=user_id)
            ticket = Ticket.objects.get(id=ticket.pk)
            chat_id = ticket.chat.tg_chat_id

            MessageOut.objects.create(user=user, ticket_id=ticket, text=text)
            send_telegram_message(chat_id, text)

            return {"status": "sent"}

        except Exception as e:
            raise ValueError(f"Ошибка OperatorService reply: {str(e)}")
