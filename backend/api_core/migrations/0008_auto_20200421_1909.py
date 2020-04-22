# Generated by Django 3.0.3 on 2020-04-21 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_core', '0007_auto_20200420_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='comorbidities',
            field=models.ManyToManyField(blank=True, to='api_core.Comorbidity', verbose_name='Comorbiditati (conditii medicale existente)'),
        ),
        migrations.AlterField(
            model_name='comorbidity',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Numele conditiei medicale'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Numele spitalului'),
        ),
    ]
