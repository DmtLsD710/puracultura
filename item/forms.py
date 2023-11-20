from django import forms

from .models import Item

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'category', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'description': forms.Textarea(attrs={'placeholder': 'Descripción'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Precio'}),
            'category': forms.Select(attrs={'placeholder': 'Categoría'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Imagen'}),
        }
