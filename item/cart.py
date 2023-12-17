from django.conf import settings
from .models import Item

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        user = request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # Create a unique session key for each user
            cart_session_id = f"{settings.CART_SESSION_ID}_{user.id}"
        else:
            # Use a generic cart session ID for anonymous users
            cart_session_id = settings.CART_SESSION_ID

        cart = self.session.get(cart_session_id)

        if not cart:
            cart = self.session[cart_session_id] = {}

        self.cart = cart
        self.cart_session_id = cart_session_id  # Store the unique session key

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Item.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['total_price'] = int(item['product'].price * item['quantity']) / 100
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)
        product = Item.objects.get(pk=product_id)
        cart_quantity = self.cart.get(product_id, {}).get('quantity', 0)

        if update_quantity:
            new_quantity = quantity
        else:
            new_quantity = cart_quantity + quantity

        new_quantity = min(new_quantity, product.stock)

        self.cart[product_id] = {'quantity': new_quantity, 'id': product_id}
        self.save()

    def remove(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
        self.save()

    def get_subtotal(self):
        subtotal = sum(Item.objects.get(id=item['id']).price * item['quantity'] for item in self.cart.values())
        return subtotal
    
    def get_iva(self):
        subtotal = self.get_subtotal()  
        iva = subtotal * 0.13
        return iva
    
    def get_total_cost(self):
        subtotal = self.get_subtotal()  
        iva = self.get_iva()
        total_cost = subtotal + iva
        return total_cost

    def save(self):
        self.session[self.cart_session_id] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[self.cart_session_id]
        self.session.modified = True
