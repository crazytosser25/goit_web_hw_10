# Generated by Django 5.1 on 2024-08-25 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotesapp', '0004_alter_quote_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='text',
            field=models.CharField(max_length=3000),
        ),
    ]
