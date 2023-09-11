from .models import ModelisReview,User, Profilis
from django import forms



class ModelisReviewForm(forms.ModelForm):
    class Meta:
        model = ModelisReview
        fields = ('content', 'modelis', 'reviewer')
        whidgets = {
            'modelis': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']