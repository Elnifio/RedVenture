# Generated by Django 2.2.5 on 2019-11-13 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0008_movie_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('genre', models.TextField(default='')),
            ],
        ),
    ]
