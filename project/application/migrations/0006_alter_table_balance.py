# Generated by Django 4.1.5 on 2023-01-04 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_alter_table_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='Balance',
            field=models.IntegerField(null=True),
        ),
    ]
