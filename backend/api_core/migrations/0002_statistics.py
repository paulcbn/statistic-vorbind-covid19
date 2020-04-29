# Generated by Django 3.0.3 on 2020-04-28 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Continut')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Data generarii statisticii')),
                ('field', models.CharField(blank=True, max_length=25, null=True)),
                ('groups', models.CharField(blank=True, max_length=50, null=True)),
                ('filters', models.CharField(blank=True, max_length=255, null=True)),
                ('group_by_gender', models.BooleanField(default=False)),
                ('group_by_county', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Statistics',
            },
        ),
    ]
