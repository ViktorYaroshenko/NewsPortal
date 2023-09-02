from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import inform_to_subscribers_about_new_post
from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(instance, action, **kwargs):
    if action == 'post_add':
        inform_to_subscribers_about_new_post.delay(instance.id)


        # emails = [
        #     user.email
        #     for category in instance.category.all()
        #     for user in category.subscribers.all()
        # ]
        #
        # subject = f'Новая запись в категории, на которую вы подписаны'
        #
        # text_content = (
        #     f'Пост: {instance.title}\n'
        #     f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        # )
        # html_content = (
        #     f'Запись: {instance.title}<br>'
        #     f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        #     f'Ссылка на новый пост</a>'
        # )
        # for email in emails:
        #     msg = EmailMultiAlternatives(subject, text_content, None, [email])
        #     msg.attach_alternative(html_content, "text/html")
        #     msg.send()