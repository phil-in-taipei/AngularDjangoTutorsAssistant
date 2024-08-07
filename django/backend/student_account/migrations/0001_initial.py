# Generated by Django 4.2.13 on 2024-07-13 06:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import utilities.general_utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentOrClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_or_class_name', models.CharField(max_length=200)),
                ('account_type', models.CharField(choices=[('freelance', 'Freelance'), ('School', 'School')], default='freelance', max_length=200)),
                ('comments', models.TextField(blank=True, default='', validators=[django.core.validators.MaxLengthValidator(500)])),
                ('purchased_class_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('tuition_per_hour', models.PositiveSmallIntegerField(default=900, validators=[utilities.general_utils.validate_tuition_rate])),
                ('account_id', models.CharField(blank=True, max_length=10, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to='user_profiles.userprofile')),
            ],
            options={
                'ordering': ('teacher__surname', 'student_or_class_name'),
                'unique_together': {('teacher', 'student_or_class_name')},
            },
            managers=[
                ('custom_query', django.db.models.manager.Manager()),
            ],
        ),
    ]
