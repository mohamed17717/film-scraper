# Generated by Django 2.1.4 on 2018-12-20 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, unique=True)),
                ('year', models.CharField(max_length=4)),
                ('mpaa', models.CharField(blank=True, max_length=20, null=True)),
                ('length', models.CharField(blank=True, max_length=20, null=True)),
                ('category', models.CharField(blank=True, max_length=60, null=True)),
                ('poster', models.URLField(blank=True, null=True)),
                ('trailer', models.URLField(blank=True, null=True)),
                ('brief_en', models.TextField(blank=True, null=True)),
                ('brief_ar', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('rating', models.TextField(blank=True, null=True)),
                ('reviews', models.TextField(blank=True, null=True)),
                ('cast', models.TextField(blank=True, null=True)),
                ('torrent', models.TextField(blank=True, null=True)),
                ('download', models.TextField(blank=True, null=True)),
                ('subtitle', models.TextField(blank=True, null=True)),
                ('prizes_won', models.TextField(blank=True, null=True)),
                ('prizes_nomenee', models.TextField(blank=True, null=True)),
                ('trust', models.BooleanField(default=False)),
                ('trusted', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'FilmInformation',
                'verbose_name_plural': 'FilmInformations',
                'db_table': '',
                'managed': True,
            },
        ),
    ]