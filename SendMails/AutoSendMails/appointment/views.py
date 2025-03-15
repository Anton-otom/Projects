from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail, mail_managers
from datetime import datetime

from django.template.loader import render_to_string
from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # send_mail(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     message=appointment.message,
        #     from_email='anthon.sev@yandex.ru',
        #     recipient_list=['an.vaseko@mail.ru']
        # )


        # html_content = render_to_string(
        #     'appointment_created.html',
        #     {
        #         'appointment': appointment,
        #     }
        # )
        #
        # msg = EmailMultiAlternatives(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     body=appointment.message,
        #     from_email='anthon.sev@yandex.ru',
        #     to=['an.vaseko@mail.ru'],
        # )
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()


        # mail_admins(
        #     subject=f'Рассылка для админов {appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
        #     message=appointment.message,
        # )


        # mail_managers(
        #     subject=f'Рассылка для менеджеров {appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
        #     message=appointment.message,
        # )


        # return redirect('make_appointment')
