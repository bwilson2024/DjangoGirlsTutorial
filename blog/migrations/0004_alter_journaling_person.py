# Generated by Django 3.2.25 on 2024-04-28 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_journaling_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journaling',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to='blog.person'),
        ),
    ]
