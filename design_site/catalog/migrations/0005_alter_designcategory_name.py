# Generated by Django 4.2.6 on 2023-11-06 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designcategory',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]