from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from weasyprint import HTML
from .helper.data_helper import get_daily_report_info as daily_report
from django.views.generic.edit import FormView, UpdateView

from .models import Report
from .forms import ReportForm

class FrontendRenderView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dailies/home.html', {})

class IndexTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_reports = Report.objects.filter(user_pk=request.user.id)
            return render(request, 'dailies/index.html', {'user_reports':user_reports})
        else:
            return HttpResponseRedirect('/login/')

class EditReportView(UpdateView):
    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         report = daily_report(self.kwargs.get('pk'))
    #         return render(request, "dailies/edit_report.html", {'report':report})
    #     else:
    #         return HttpResponseRedirect('/dailies/')

    template_name = 'dailies/edit_report.html'
    form_class = ReportForm
    success_url = '/dailies/'

    def get_initial(self):
        report = daily_report(self.kwargs.get('pk'))
        return {'your_name': 'test'}

    def get_success_url(self):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)

class ReportView(TemplateView):
    def to_pdf(self, report):
        html_string = render_to_string('dailies/report.html', {'report': report})
        html = HTML(string=html_string)
        pdf_name = 'Report_' + report['date'].replace('-','_') + '.pdf'
        html.write_pdf(target='dailies/tmp/' + pdf_name);

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            report = daily_report(self.kwargs.get('pk'))
            self.to_pdf(report)
            return render(request, 'dailies/report.html', {'report':report})
        else:
            return HttpResponseRedirect('/dailies/')
