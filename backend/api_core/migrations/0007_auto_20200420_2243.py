# Generated by Django 3.0.3 on 2020-04-20 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_core', '0006_auto_20200420_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='test_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data recoltarii probei'),
        ),
        migrations.AlterField(
            model_name='case',
            name='collision_index',
            field=models.PositiveIntegerField(verbose_name='Indice suprapunere'),
        ),
        migrations.AlterField(
            model_name='case',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='Deces validat manual'),
        ),
    ]
