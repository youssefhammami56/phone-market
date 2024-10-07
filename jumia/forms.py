from django import forms

class SearchForm(forms.Form):
    brand = forms.CharField(label='Marque', max_length=100)
    max_price = forms.IntegerField(label='Prix maximal')
