# Generated by Django 5.1.2 on 2024-11-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_userprofile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='house_no',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(default='9999999999', max_length=10, unique=True),
        ),
    ]
