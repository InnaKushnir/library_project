# Generated by Django 4.1.7 on 2023-10-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_readingsession"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="full_description",
            field=models.TextField(default="Good book", max_length=2056),
        ),
    ]
