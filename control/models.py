import datetime
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save,post_delete,pre_save
from simple_history.models import HistoricalRecords
# Create your models here.
welayats = (
    ('J',"Jemlenýär"),
    ("Mary", "Mary"),
    ("Aşgabat", "Aşgabat"),
    ("Lebap", "Lebap"),
    ("Daşoguz", "Daşoguz"),
    ("Balkan", "Balkan"),
)
payment_type = (
    ("N", "Nagt"),
    ("C", "Terminal"),
    ("O", "Online"),
)
status = (
    ("P","📦"),
    ("D","❌"),
    ("H","❗"),
    ("S","✅")
)

class Cash_registers(models.Model):
    name = models.CharField(max_length=20, verbose_name='Kassanyň ady')
    address = models.CharField(max_length=100, blank=True,null=True, verbose_name='Adress')
    balance = models.FloatField(default=0, verbose_name='Balans')
    history = HistoricalRecords()
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kassa'
        verbose_name_plural = 'Kassalar'


class Order(models.Model):
    code = models.CharField(max_length=50, default='1',verbose_name='Sargydyň kody')
    time = models.DateField(default=datetime.datetime.now,verbose_name='Sargyt edilen wagty')
    initial_dest = models.CharField(max_length=50, choices=welayats,default='J',verbose_name='Duran ýeri')
    cash_registry = models.ForeignKey(Cash_registers, on_delete=models.PROTECT,blank=True,null=True,verbose_name="Kassa")
    final_dest = models.CharField(max_length=50, choices=welayats,verbose_name='Barmaly ýeri')
    payment_type = models.CharField(max_length=50, choices=payment_type,default='N',verbose_name='Töleg')
    initial_price = models.FloatField(blank=True, null=True,verbose_name="Asyl töleg")
    final_price = models.FloatField(blank=True, null=True,verbose_name='Müşderiniň töläni')
    service_fee = models.FloatField(max_length=50,default=0,verbose_name='Eltip Bermek')
    status = models.CharField(max_length=50,choices=status,default='P')
    in_center = models.BooleanField(default=False,verbose_name='Merkezdemi?')
    in_center_update = models.DateTimeField(default=datetime.datetime.now,verbose_name='Merkeze geçen wagty')
    in_balance = models.BooleanField(default=True,verbose_name='Balansdamy?')

    def calculate_total_price(self):
        initial_total = sum(item.item_price * item.initial_quantity for item in self.order_item_set.all()) + self.service_fee
        if self.order_item_set.filter(final_quantity=None):
            final_total = None
        else:
            if sum(item.item_price * item.final_quantity for item in self.order_item_set.all())!=0:
                final_total = sum(item.item_price * item.final_quantity for item in self.order_item_set.all()) + self.service_fee
                self.cash_registry = Cash_registers.objects.get(name=self.final_dest)
            else:
                final_total = 0
                self.cash_registry = Cash_registers.objects.get(name=self.final_dest)
            if self.payment_type == 'N' and self.in_center != True and self.cash_registry.name != 'Mary':
                self.cash_registry.balance += final_total
                self.cash_registry.save()
            elif self.payment_type =='N' and self.cash_registry.name == 'Mary':
                self.cash_registry = Cash_registers.objects.get(name='Mary')
                self.cash_registry.balance += final_total
                self.in_center = True
                self.in_center_update = datetime.datetime.now()
                self.cash_registry.save()
            elif self.payment_type !='N':
                pass
        self.initial_price = initial_total
        self.final_price = final_total
        self.save()

    def status_changer(self):
        if self.order_item_set.filter(final_quantity=None):
            pass
        else:
            if self.final_price is None:
                self.status = 'P'
            elif self.final_price == self.initial_price:
                self.status = 'S'
            elif 0 < self.final_price < self.initial_price:
                self.status = 'H'
            elif self.final_price == 0:
                self.status = 'D'
        self.save()

    def destination_changer(self):
        all_in_one_place = True
        if self.initial_dest == 'J':
            for item in self.order_item_set.all():
                if item.initial_dest != item.final_dest:
                    all_in_one_place = False
                    place = item.initial_dest
            if all_in_one_place:
                self.initial_dest = self.order_item_set.all()[0].initial_dest
        self.save()




    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Sargyt'
        verbose_name_plural = 'Sargytlar'


class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=50,verbose_name='Harydyň kody')
    initial_dest = models.CharField(max_length=50, choices=welayats,verbose_name='Harydyň ýerleşýän ýeri')
    final_dest = models.CharField(max_length=50, choices=welayats,verbose_name='Harydyň jemlenýän ýeri')
    size = models.CharField(max_length=50, blank=True, null=True,verbose_name='Harydyň razmeri, ýok bolsa boş')
    initial_quantity = models.PositiveIntegerField(default=1,verbose_name='Harydyň mukdary')
    final_quantity = models.PositiveIntegerField(blank=True, null=True,verbose_name='Harydyň kabul edilen mukdary')
    item_price = models.FloatField(help_text='Harydyň bahasy')
    def save(self, *args, **kwargs):
        # Ensure final_quantity does not exceed initial_quantity
        if self.final_quantity is not None and self.final_quantity > self.initial_quantity:
            self.final_quantity = self.initial_quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return self.barcode

    class Meta:
        verbose_name = 'Haryt'
        verbose_name_plural = 'Harytlar'

    @property
    def total_price(self):
        return self.initial_quantity * self.item_price

    @property
    def final_price(self):
        return self.final_quantity * self.item_price



@receiver(post_save,sender=Order_item)
@receiver(post_delete, sender=Order_item)
def update_order(sender, instance, **kwargs):
    instance.order.calculate_total_price()
    instance.order.status_changer()

@receiver(post_save,sender=Order_item)
def update_destination(sender, instance, **kwargs):
    instance.order.destination_changer()






@receiver(pre_save,sender=Order)
def cash_to_center(sender,instance,*args,**kwargs):
    if instance.payment_type == 'N':
        try:
            order = Order.objects.get(id=instance.id)
            if (int(order.in_center) < int(instance.in_center)) and order.final_price:
                cash_register = order.cash_registry
                if cash_register.name != 'Mary':
                    cash_register.balance -= order.final_price
                    cash_register_mary = Cash_registers.objects.get(name='Mary')
                    cash_register_mary.balance += order.final_price
                    cash_register_mary.save()
                    cash_register.save()
                    instance.cash_registry = Cash_registers.objects.get(name='Mary')
        except:
            pass







