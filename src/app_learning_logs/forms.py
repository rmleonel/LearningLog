from django import forms 
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Topic
        fields = ["text", "image"]
        labels = {"text": "Título"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'placeholder': 'Ingresa el título aquí'})

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {"text" : ""}
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}