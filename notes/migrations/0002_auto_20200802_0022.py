# Generated by Django 3.0.8 on 2020-08-02 00:22

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note',
            field=fernet_fields.fields.EncryptedTextField(),
        ),
    ]
