from django import forms
from .models import Student
from .models import Grade
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # This tells Django which fields to put on the website
        fields = ['first_name', 'last_name', 'email', 'age', 'major']
        
        # This adds Bootstrap styling to the input boxes
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score']
        # Styling it with Bootstrap classes
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mathematics'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
        }