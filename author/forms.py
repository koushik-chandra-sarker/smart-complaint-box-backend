
from django import forms


class MailInfoForm(forms.ModelForm):
    class Meta:
        widgets = {
            'password': forms.PasswordInput()
        }
        fields = '__all__'

