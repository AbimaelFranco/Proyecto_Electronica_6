# Generated by Django 4.1.1 on 2023-04-28 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoApp', '0003_static_panel_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='static_panel',
            name='intensity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='static_panel',
            name='measurement',
            field=models.FloatField(default=0),
        ),
    ]
