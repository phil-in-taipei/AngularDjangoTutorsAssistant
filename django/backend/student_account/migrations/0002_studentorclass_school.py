# Generated by Django 4.2.13 on 2024-07-13 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
        ('student_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentorclass',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school', to='school.school'),
        ),
    ]