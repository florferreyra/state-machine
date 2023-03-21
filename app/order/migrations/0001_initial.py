# Generated by Django 4.1.7 on 2023-03-21 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.CharField(max_length=200)),
                ('client_id', models.CharField(max_length=10)),
                ('state', models.CharField(choices=[('created', 'created'), ('waiting_for_payment', 'waiting_for_payment'), ('processing', 'processing'), ('shipping', 'shipping'), ('completed', 'completed'), ('canceled', 'canceled')], default='created', max_length=50)),
            ],
        ),
    ]