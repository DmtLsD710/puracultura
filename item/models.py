# Importamos los módulos necesarios de Django
from django.db import models
from django.conf import settings

# Definimos el modelo Category
class Category(models.Model):
    # Cada categoría tiene un nombre
    name = models.CharField(max_length=255, verbose_name='Nombre')
    
    class Meta:
        # Las categorías se ordenan por su nombre
        ordering = ('name',)
        # El nombre plural en español para el modelo es 'Categorías'
        verbose_name_plural = 'Categorías'
        
    # La representación en cadena de una categoría es su nombre
    def __str__(self):
        return self.name
    
# Definimos el modelo Item
class Item(models.Model):
    # Cada item pertenece a una categoría
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE, verbose_name='Categoría')
    # Cada item tiene un nombre, descripción, precio, imagen, creador, fecha de creación y stock
    name = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    price = models.FloatField(verbose_name='Precio')
    image = models.ImageField(upload_to='item_images', blank=True, null=True, verbose_name='Imagen')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE, verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    stock = models.PositiveIntegerField(default=1, verbose_name='Inventario')
    
    # Propiedad que indica si el item está vendido (si el stock es 0)
    @property
    def is_sold(self):
        return self.stock == 0
    
    class Meta:
        # Los items se ordenan por su nombre
        ordering = ('name',)  
        
    # La representación en cadena de un item es su nombre
    def __str__(self):
        return self.name

# Definimos el modelo Review
class Review(models.Model):
    # Las opciones de calificación para una revisión
    RATING_CHOICES = (
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

    # Cada revisión pertenece a un item y tiene un autor, contenido, calificación y fecha de creación
    item = models.ForeignKey('Item', related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # La representación en cadena de una revisión es 'Review by {author} for {item}'
    def __str__(self):
        return f'Review by {self.author.username} for {self.item.name}'