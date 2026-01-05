from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Mailing, Message, Recipient, SendAttempt


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="RUNNING").count()
    unique_recipients = Recipient.objects.count()
    return render(
        request,
        "../templates/MailingListManagement/home.html",
        {
            "total_mailings": total_mailings,
            "active_mailings": active_mailings,
            "unique_recipients": unique_recipients,
        },
    )


class RecipientListView(ListView):
    model = Recipient
    template_name = "../templates/MailingListManagement/recipient_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("can_view_recipient"):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "../templates/MailingListManagement/recipient_detail.html"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = Recipient
    success_url = reverse_lazy("mailing_list_management:recipient_list")

    def form_valid(self, form):
        product = form.save(commit=False)
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    template_name = "../templates/MailingListManagement/recipient_form.html"
    success_url = reverse_lazy("mailing_list_management:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mailing_list_management:recipient_list")


class MessageListView(ListView):
    model = Message
    template_name = "../templates/MailingListManagement/message_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("can_view_message"):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    template_name = "../templates/MailingListManagement/message_detail.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    success_url = reverse_lazy("mailing_list_management:recipient_list")

    def form_valid(self, form):
        product = form.save(commit=False)
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    success_url = reverse_lazy("mailing_list_management:recipient_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing_list_management:recipient_list")


class MailingListView(ListView):
    model = Mailing
    template_name = "../templates/MailingListManagement/mailing_list.html"

    def get_queryset(self):
        if self.request.user.has_perm("can_view_mailing"):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "../templates/MailingListManagement/mailing_detail.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    success_url = reverse_lazy("mailing_list_management:recipient_list")

    def form_valid(self, form):
        product = form.save(commit=False)
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    success_url = reverse_lazy("mailing_list_management:recipient_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailing_list_management:recipient_list")


def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    recipients = mailing.recipients.all()
    send_attempt = SendAttempt(mailing=mailing)

    for recipient in recipients:
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                "from@example.com",
                [recipient.email],
            )
            send_attempt.status = "SUCCESS"
            send_attempt.server_response = "Mail sent"
        except Exception as e:
            send_attempt.status = "FAIL"
            send_attempt.server_response = str(e)
        finally:
            send_attempt.save()
