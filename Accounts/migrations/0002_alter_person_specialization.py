# Generated by Django 4.2.1 on 2023-05-16 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="Specialization",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
