from django import forms
from .models import newsDetails, Category, todoList, webScraping, Semrush

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
        self.fields['newsCategory'].empty_label = "Select"
        self.fields['newsChannel'].required = False

class NewsCat(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title',)
        labels = {
            'id': 'id',
            'title' : 'News Category Title'
        }
    
class listForm(forms.ModelForm):

    class Meta:
        model = todoList
        fields = ('title',)

class ScrapperForm(forms.ModelForm):
    class Meta:
        model = webScraping
        fields = ['url']
        widgets = {
            'url' : forms.TextInput(attrs={'class':'form-control'}),
        }
