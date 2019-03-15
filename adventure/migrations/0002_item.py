# Generated by Django 2.1.2 on 2018-11-01 18:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
    ]