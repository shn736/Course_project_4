from django.db import models
from django.utils import timezone

from users.models import User


class Recipient(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Эл. почта",
        help_text="Введите свою электронную почту",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Имя получателя рассылки",
        help_text="Введите имя получателя рассылки",
    )
    comment = models.TextField(
        blank=True,
        max_length=55,
        verbose_name="Комментарий",
        help_text="Введите комментарий",
    )

    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца товара",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        permissions = [("can_view_recipient", "can view recipient")]

    def __str__(self):
        return self.name


class Message(models.Model):
    subject = models.CharField(
        max_length=255, verbose_name="Тема письма", help_text="Введите тему письма"
    )
    body = models.TextField(
        max_length=255, verbose_name="Тело письма", help_text="Введите тело письма"
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца товара",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [("can_view_message", "can view message")]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "Создана"),
        ("RUNNING", "Запущена"),
        ("COMPLETED", "Завершена"),
    ]

    start_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name="Дата и время начала отправки",
        help_text="Введите дату и время начала отправки",
    )
    end_time = models.DateTimeField(
        default=timezone.now,
        blank=True,
        null=True,
        verbose_name="Дата и время окончания отправки",
        help_text="Введите дату и время окончания отправки",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="CREATED",
        verbose_name="Статус",
        help_text="Введите статус",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Сообщение",
        help_text="Укажите Сообщение",
    )
    recipients = models.ManyToManyField(
        Recipient,
        verbose_name="Имя получателя рассылки",
        help_text="Введите имя получателя рассылки",
    )

    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца товара",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Mailing: {self.message.subject}"


class SendAttempt(models.Model):
    ATTEMPT_STATUS_CHOICES = [
        ("SUCCESS", "Успешно"),
        ("FAIL", "Не успешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ATTEMPT_STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        permissions = [("can_view_mailing", "can view mailing")]

    def __str__(self):
        return f"Attempt: {self.status} at {self.attempt_time}"
