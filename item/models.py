from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categorías'
        
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE, verbose_name='Categoría')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    price = models.FloatField(verbose_name='Precio')
    image = models.ImageField(upload_to='item_images', blank=True, null=True, verbose_name='Imagen')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE, verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    stock = models.PositiveIntegerField(default=1, verbose_name='Inventario')
    
    @property
    def is_sold(self):
        return self.stock == 0
    
    class Meta:
        ordering = ('name',)  
        
    def __str__(self):
        return self.name

class Review(models.Model):
    RATING_CHOICES = (
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

    item = models.ForeignKey('Item', related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.author.username} for {self.item.name}'