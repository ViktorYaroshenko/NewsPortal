from celery import shared_task
import time
import datetime
from news.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def inform_to_subscribers_about_new_post(instance_id):
    instance = Post.objects.get(pk=instance_id)
    emails = [
        user.email
        for category in instance.category.all()
        for user in category.subscribers.all()
    ]

    subject = f'Новая запись в категории, на которую вы подписаны'

    text_content = (
        f'Пост: {instance.title}\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Запись: {instance.title}<br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на новый пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def every_week_mailing():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)

    categories = set(posts.values_list('category__id', flat=True))
    email_of_subscribers = set(
        Subscriptions.objects.filter(category_id__in=categories).values_list('user__email', flat=True))

    for every_subscriber in email_of_subscribers:
        send_email = []
        categories_for_one_subscriber = set(
            Subscriptions.objects.filter(user__email=every_subscriber).values_list('category_id', flat=True))
        posts_for_only_this_subscriber = posts.filter(category__id__in=categories_for_one_subscriber)
        send_email.append(every_subscriber)

        html_content = render_to_string('week_posts.html',
                                        {'posts': posts_for_only_this_subscriber,
                                         })
        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=send_email,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
