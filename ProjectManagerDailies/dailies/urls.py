from django.urls import path

from . import views

app_name = 'dailies'
urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('report/<int:pk>/view', views.ReportView.as_view(), name='report'),
    path('report/<int:pk>/edit', views.EditReportView.as_view(), name='edit_report'),
]
