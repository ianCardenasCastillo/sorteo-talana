# Generated by Django 3.2.3 on 2021-05-19 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorteo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]