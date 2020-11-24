from django import forms
from .models import newsDetails

class NewsForm(forms.ModelForm):

    class Meta:
        model = newsDetails
        fields = ('newsTitle', 'newsCategory', 'newsDescription', 'newsChannel')
        labels = {
            'newsTitle' : 'News Title',
            'newsCategory' : 'News Category',
            'newsDescription' : 'News Description',
            'newsChannel' : 'News Channel'
        }

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['newsChannel'].required = False
        