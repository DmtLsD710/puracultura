# Importamos el módulo forms de Django
from django import forms

# Importamos el modelo Item de nuestro módulo models
from .models import Item

# Definimos una nueva forma llamada NewItemForm que hereda de forms.ModelForm
class NewItemForm(forms.ModelForm):
    # Dentro de la clase definimos una subclase Meta
    class Meta:
        # Especificamos que el modelo a utilizar es Item
        model = Item
        # Definimos los campos del modelo que queremos incluir en el formulario
        fields = ('name', 'description', 'price', 'category', 'image')
        # Definimos los widgets para los campos del formulario. Esto nos permite personalizar cómo se renderizan los campos.
        widgets = {
            # Para el campo 'name', usamos un TextInput y establecemos el atributo 'placeholder' a 'Nombre'
            'name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            # Para el campo 'description', usamos un Textarea y establecemos el atributo 'placeholder' a 'Descripción'
            'description': forms.Textarea(attrs={'placeholder': 'Descripción'}),
            # Para el campo 'price', usamos un NumberInput y establecemos el atributo 'placeholder' a 'Precio'
            'price': forms.NumberInput(attrs={'placeholder': 'Precio'}),
            # Para el campo 'category', usamos un Select y establecemos el atributo 'placeholder' a 'Categoría'
            'category': forms.Select(attrs={'placeholder': 'Categoría'}),
            # Para el campo 'image', usamos un ClearableFileInput y establecemos el atributo 'placeholder' a 'Imagen'
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Imagen'}),
        }