# Generated by Django 3.2.7 on 2021-09-15 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('topics', models.ManyToManyField(to='docstore.Topic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='', verbose_name='/home/pbravo/Documents/interview/docustore/media')),
                ('folder_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='docstore.folder')),
                ('topics', models.ManyToManyField(to='docstore.Topic')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
