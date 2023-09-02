# Generated by Django 4.2.3 on 2023-08-06 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0007_category_subscribers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
    ]
