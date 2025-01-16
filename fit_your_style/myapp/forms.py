from django import forms
from .models import Appointment

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = [ 'date', 'time', 'message', 'picture']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
#             'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['store', 'date', 'time', 'message', 'picture']
        widgets = {
            'store': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



