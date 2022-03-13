from datetime import timedelta
import time
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from django.core.mail import send_mail
from pytz import timezone
from task_manager.celery import app

from tasks.models import STATUS_CHOICES, Report, Task, User


@periodic_task(run_every=timedelta(seconds=10))
def send_email_reminder():
    time_now = datetime.now(timezone("UTC"))
    reports = Report.objects.filter(timestamp__lte=time_now, is_disabled=False)
    for report in reports:
        user = User.objects.get(id=report.user.id)
        subject = user.username + "'s Task Report"
        all_tasks = Task.objects.filter(deleted=False, user=user)
        content = f"Hi {user.username}! Here is your task report:\n\n\n"
        for i in range(len(STATUS_CHOICES) - 1):
            tasks = all_tasks.filter(status=STATUS_CHOICES[i][0])
            content += (
                f"YOUR {STATUS_CHOICES[i][0].title()} TASKS :  {str(tasks.count())}\n"
            )
            for i in range(len(tasks)):
                content += f"{i + 1}) {tasks[i]}\n"
            content += "\n\n"
        send_mail(
            subject,
            content,
            "aayushimittal025@gmail.com",
            "aayushimittal025@gmail.com",
        )
        report.timestamp = report.timestamp + timedelta(days=1)
        report.save()
        print("Email sent!")
