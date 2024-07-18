from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=150, null=False)
    address = models.JSONField(null=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Cart(models.Model):
    customer = models.ForeignKey('shop.Customer', on_delete=models.CASCADE, null=False)
    create_date = models.DateTimeField(auto_now_add=True, null=False)
    expired_in = models.IntegerField(null=False, default=60)

    def __str__(self) -> str:
        return f'Customor ID: {self.customer} Cart ID: {self.id}'
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=150, null=False)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True)
    remaining_amount = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    categories = models.ManyToManyField("shop.ProductCategory")

    def __str__(self) -> str:
        return f'Product name: {self.name}\nDescription: {self.description}\nRemianing: {self.remaining_amount}\nPrice: {self.price}\nCategories: {self.categories}'
    
class Cartitem(models.Model):
    cart = models.ForeignKey('shop.cart', on_delete=models.CASCADE, null=False)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT, null=False)
    amount = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f'{self.cart} {self.product} {self.amount}'

class Order(models.Model):
    customer = models.ForeignKey('shop.Customer', on_delete=models.PROTECT, null=False)
    order_date = models.DateField(auto_now_add=True, null=False)
    remark = models.TextField(null=True)

    def __str__(self) -> str:
        return f'Order ID: {self.id} Customer ID: {self.customer}'
    
class OrderItem(models.Model):
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE, null=False)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT, null=False)
    amount = models.IntegerField(null=True, default=1)

    def __str__(self) -> str:
        return f'{self.order} {self.product} {self.amount}'
    
class Payment(models.Model):
    order = models.OneToOneField('shop.Order', on_delete=models.PROTECT, null=False)
    payment_date = models.DateField(auto_now_add=True, null=False)
    remark = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

class PaymentItem(models.Model):
    payment = models.ForeignKey('shop.Payment', on_delete=models.CASCADE, null=False)
    order_item = models.OneToOneField('shop.OrderItem', on_delete=models.PROTECT, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

class PaymentMethod(models.Model):
    payment = models.ForeignKey('shop.Payment', on_delete=models.CASCADE, null=False)
    QR = 'QR'
    CREDIT = 'CREDIT'
    payment_choice = {
        QR: "QR",   
        CREDIT: "CREDIT",
    }
    method = models.CharField(choices=payment_choice, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
