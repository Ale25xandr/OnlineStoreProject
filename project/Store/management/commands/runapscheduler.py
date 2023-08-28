import datetime
import logging
import random
from datetime import datetime, timedelta
import pytz

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from Store.models import Ads

logger = logging.getLogger(__name__)


def my_job():
    d_1 = datetime(year=datetime.now().year,
                   month=datetime.now().month,
                   day=datetime.now().day,
                   hour=0,
                   minute=0,
                   second=0,
                   tzinfo=pytz.UTC)
    d_2 = d_1 - timedelta(days=7)
    ads = Ads.objects.filter(Date__range=[d_2, d_1])
    ads_1 = random.sample(list(ads), 5)
    print(ads_1)
    user = User.objects.all()
    email = []
    for i in range(0, len(user)):
        if user[i].email:
            email.append(user[i].email)

    subject = f'Объявления за прошедшую неделю'
    message = ''
    from_email = 'Foma26199622@mail.ru'

    mail = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_email,
        to=email,
    )

    html = render_to_string('send_ads.html',
                            context={'ads': ads_1})

    print(html)

    mail.attach_alternative(html, 'text/html')

    mail.send()


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="*/1"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
