from .models import ModelisReview
from django import forms


class ModelisReviewForm(forms.ModelForm):
    class Meta:
        model = ModelisReview
        fields = ('content', 'modelis', 'reviewer')
        whidgets = {
            'modelis': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }