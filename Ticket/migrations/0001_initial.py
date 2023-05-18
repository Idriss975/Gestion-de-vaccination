# Generated by Django 4.2.1 on 2023-05-16 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vaccine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=20)),
                ("Virus", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Time", models.DateTimeField()),
                ("Location", models.CharField(max_length=50)),
                (
                    "Status",
                    models.CharField(
                        choices=[
                            ("C", "Created"),
                            ("C", "Confirmed"),
                            ("C", "Cancelled"),
                        ],
                        max_length=9,
                    ),
                ),
                (
                    "Vaccine",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Ticket.vaccine",
                    ),
                ),
            ],
        ),
    ]
