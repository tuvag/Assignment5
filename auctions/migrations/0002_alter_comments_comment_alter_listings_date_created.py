# Generated by Django 4.1.2 on 2022-10-24 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='listings',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
