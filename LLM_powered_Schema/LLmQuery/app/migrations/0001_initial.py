# Generated by Django 5.1.1 on 2025-02-22 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('supplier', models.CharField(max_length=255)),
                ('store', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('discount_pcnt', models.IntegerField()),
            ],
        ),
    ]
