# Generated by Django 2.0.7 on 2018-07-30 22:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dailies', '0002_auto_20180730_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.TextField()),
                ('task_details', models.TextField()),
                ('task_hours', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment_Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_used', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Project Name')),
                ('number', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('weather', models.CharField(max_length=200, verbose_name='Weather')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailies.Project')),
            ],
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Equipment Name'),
        ),
        migrations.AddField(
            model_name='equipment_report',
            name='equipment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailies.Equipment'),
        ),
        migrations.AddField(
            model_name='equipment_report',
            name='report_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailies.Report'),
        ),
        migrations.AddField(
            model_name='employee_report',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailies.Employee'),
        ),
        migrations.AddField(
            model_name='employee_report',
            name='report_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dailies.Report'),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together={('number', 'user')},
        ),
    ]
