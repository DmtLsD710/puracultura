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
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Item.objects.get(pk=p)
        
        for item in self.cart.values():
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

    def get_total_cost(self):
        total_cost = 0
        for p in self.cart.keys():
            self.cart[str(p)]['product'] = Item.objects.get(pk=p)
            total_cost += self.cart[str(p)]['product'].price * self.cart[str(p)]['quantity'] 
            tax_cost = (total_cost * 0.13) + total_cost
        return round(tax_cost, 2)

    def save(self):
        self.session[self.cart_session_id] = self.cart
        self.session.modified = True
        self.session.save()
