from django import forms

class ReportForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass