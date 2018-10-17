from django.conf import settings
from django.db import models


class Contractor(models.Model):
    ctr_code = models.CharField(max_length=10, primary_key=True, verbose_name="Contractor Code")
    company_name = models.CharField(max_length=150, verbose_name="Contractor Company Name")

    def __str__(self):
        return self.company_name


class Employee(models.Model):
    # id is the primary_key
    first_name = models.CharField(max_length=25, verbose_name="First Name")
    last_name = models.CharField(max_length=25, verbose_name="Last Name")
    labor_class = models.CharField(max_length=10, verbose_name="Labor Class")
    ctr_code = models.ForeignKey('Contractor', on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Employee_Report(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100, verbose_name= "Task Name")
    task_details = models.TextField(verbose_name= "Task Details")
    task_hours = models.DecimalField(decimal_places=1, max_digits=4, verbose_name= "Task Hours")

    def __str__(self):
        return '%s %s\'s Report - %s' % (self.employee.first_name, self.employee.last_name, str(self.report.date))


class Equipment(models.Model):
    name = models.CharField(max_length=100, verbose_name="Equipment Name")
    ctr_code = models.ForeignKey('Contractor', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Equipment_Report(models.Model):
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    hours_used = models.DecimalField(decimal_places=1, max_digits=4, verbose_name="Hours Used")

    def __str__(self):
        return '%s Report - %s' % (self.equipment.name, str(self.report.date))


class Report(models.Model):
    date = models.DateField(verbose_name="Date")
    weather = models.CharField(max_length=200, verbose_name="Weather")
    user_pk = models.IntegerField(verbose_name="User PK")
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return '%s Report - %s' % (self.project.name, str(self.date))


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Project Name")
    number = models.IntegerField(verbose_name="Project Number")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        return self.name
