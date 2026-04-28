from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'message']
        labels = {
            'name': 'Full Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number',
            'message': 'Message',
        }
        shared = 'block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500'
        widgets = {
            'name': forms.TextInput(attrs={'class': shared, 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': shared, 'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'class': shared, 'placeholder': '+254 ...'}),
            'message': forms.Textarea(attrs={'class': shared, 'rows': 5, 'placeholder': "I'd like to learn more about Harmony..."}),
        }
