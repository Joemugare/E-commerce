from django import forms
from reviews.models import Review  # Import Review from reviews app

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'comment', 'rating', 'video_url']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'title': forms.TextInput(attrs={'placeholder': 'Enter review title'}),
            'video_url': forms.URLInput(attrs={'placeholder': 'Optional video URL'}),
        }