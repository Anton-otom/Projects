from django.db import models
from datetime import datetime, timezone


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount


# cap = Product(name = "Монитор", price = 9999.0)
# cap.save()
# cap_big = Product.objects.create(name = "Монитор", price = 9999.0)
# product_1 = Product(name="Витая пара (3 м)", price=993.0)
# product_1.save()
# product_2 = Product.objects.create(name="Клавиатура", price=1060.0)
# cashier1 = Staff.objects.create(full_name="Иванов Иван Иванович",
#                                 position=Staff.cashier,
#                                 labor_contract=1754)
# cashier2 = Staff.objects.create(full_name="Петров Петр Петрович",
#                                 position=Staff.cashier,
#                                 labor_contract=4355)
# direct = Staff.objects.create(full_name="Максимов Максим Максимович",
#                               position=Staff.director,
#                               labor_contract=1254)
