# Generated by Django 3.2.25 on 2024-04-28 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_auto_20240424_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journaling',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to=settings.AUTH_USER_MODEL),
        ),
    ]
