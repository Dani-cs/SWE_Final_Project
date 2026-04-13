from django import forms
from django.forms import inlineformset_factory
from .models import List, ListItem


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title', 'list_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Give your list a title...'}),
            'list_type': forms.RadioSelect(),
        }


ListItemFormSet = inlineformset_factory(
    List,
    ListItem,
    fields=['text'],
    extra=5,
    min_num=1,
    validate_min=True,
    can_delete=True,
    widgets={'text': forms.TextInput(attrs={'placeholder': 'Add an item...'})}
)
