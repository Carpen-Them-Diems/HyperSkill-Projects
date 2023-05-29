from django import forms


class CreateArticleForm(forms.Form):
    title = forms.CharField(label='Article Title', max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Enter article title here:',
        'required': True,
        'id': 'form-textinput',
        'class': 'form-textinput',
    }))
    text = forms.CharField(label='Article Content', max_length=3000, widget=forms.Textarea(attrs={
        'placeholder': 'Enter article content here:',
        'required': True,
        'id': 'form-textarea',
        'class': 'form-textarea',
    }))
