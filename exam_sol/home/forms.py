from django import forms
from home.models import News

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('email',) 

