# Generated by Django 4.2.2 on 2023-09-07 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('motociklai', '0006_remove_modelis_aprasymas_modelis_modelis_aprasymas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelisinstance',
            name='modelis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modelisinstance_set', to='motociklai.modelis'),
        ),
    ]