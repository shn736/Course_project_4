from django.contrib import admin

from .models import Mailing, Message, Recipient, SendAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("status",)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "comment",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "body",
    )


@admin.register(SendAttempt)
class SendAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "server_response",
        "mailing",
    )
