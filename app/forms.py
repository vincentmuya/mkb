from django import forms
from .models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user