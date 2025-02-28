from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView

from config.forms import ContactForm
from content.models import HomePageContent


class HomePageView(DetailView):
    model = HomePageContent
    template_name = "home.html"
    context_object_name = "content"

    def get_object(self):
        return HomePageContent.objects.first()


class Feedback(FormView):
    """
    Представление страницы контактов
    """

    template_name = "feedback.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """
        Переопределение метода для отправки письма при успешной отправки формы
        """
        name = form.cleaned_data["name"]
        message = form.cleaned_data["message"]
        subject = f"Новое сообщение от {name}"
        recipient_list = ["lacryk@gmail.com"]

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email="lacryk@yandex.ru",
            to=recipient_list,
        )

        email.headers = {
            "Reply-To": "lacryk@yandex.ru",
        }

        email.send(fail_silently=False)

        messages.success(
            self.request, f'Спасибо, {name}! Ваше сообщение "{message}" получено.'
        )  # Добавляем сообщение об успехе
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Если форма недействительна, просто отобразим шаблон с ошибками
        """
        return super().form_invalid(form)
