# Generated by Django 5.1.7 on 2025-03-29 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.TextField()),
                ('ubication', models.CharField(choices=[('head', 'Head'), ('footer', 'Footer')], max_length=255)),
            ],
            options={
                'verbose_name': 'Integracion',
                'verbose_name_plural': 'Integraciones',
            },
        ),
    ]
