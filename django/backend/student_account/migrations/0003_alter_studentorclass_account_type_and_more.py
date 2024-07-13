# Generated by Django 4.2.13 on 2024-07-13 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_account', '0002_studentorclass_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentorclass',
            name='account_type',
            field=models.CharField(choices=[('freelance', 'Freelance'), ('school', 'School')], default='freelance', max_length=200),
        ),
        migrations.AddConstraint(
            model_name='studentorclass',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('purchased_class_hours__isnull', False), ('account_type', 'freelance')), models.Q(('school__isnull', False), ('account_type', 'school')), _connector='OR'), name='b_c_null_check'),
        ),
    ]