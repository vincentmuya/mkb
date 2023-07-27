from django import forms
from .models import Client


class DateInput(forms.DateInput):
    input_type = 'date'


class NewClientForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ["slug", "lender", "loan_balance", "loan_penalty", "is_loan_paid"]
        widgets = {
            'loan_collection_date': DateInput(),
        }

class FeedbackInquiryForm(forms.Form):
    email = forms.EmailField(required=True)
    message_content = forms.CharField(widget=forms.Textarea)