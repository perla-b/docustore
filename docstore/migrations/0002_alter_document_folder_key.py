# Generated by Django 3.2.7 on 2021-09-16 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docstore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='folder_key',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='docstore.folder'),
            preserve_default=False,
        ),
    ]