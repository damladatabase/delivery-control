import datetime
from django.contrib import admin
from control import models
from simple_history.admin import SimpleHistoryAdmin
from django.utils.html import format_html

from control.form import CashRegisterForm


@admin.action(description='Pullary merkeze geçir')
def pullary_merkeze(modeladmin, request, queryset):
    for obj in queryset:
        obj.in_center = True
        obj.in_center_update = datetime.datetime.now()
        obj.save()

class OrderInline(admin.TabularInline):
    model = models.Order
    extra = 0
    can_delete = False
    verbose_name = "Sargyt"
    verbose_name_plural = "Sargytlar"
    fields = (
        'code',
        'final_dest',
        'final_price',
        'in_center_update'
    )
    readonly_fields = (
        'code',
        'final_dest',
        'final_price',
        'in_center_update'
    )

class OrderItemInline(admin.StackedInline):
    model = models.Order_item
    extra = 0
    can_delete = True

    fieldsets = (
        ('Item Details', {'fields': ('barcode', 'size','item_price')}),
        ('Quantity and Delivery Information',{'fields': (
            'initial_quantity',
            'final_quantity',
            'initial_dest',
            'final_dest'
        )}),
    )


class CashRegisterAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = (
        'name',
        'address',
        'balance',
    )
    form = CashRegisterForm
    def save_model(self, request, obj, form, change):
        amount_to_deduct = form.cleaned_data.get('amount_to_deduct', 0)
        if amount_to_deduct:
            obj.balance -= amount_to_deduct
        obj.save()
class CashRegisterHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ["changed_fields","list_changes"]

    def changed_fields(self, obj):
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)
            return delta.changed_fields
        return None

    def list_changes(self, obj):
        fields = ""
        if obj.prev_record:
            delta = obj.diff_against(obj.prev_record)

            for change in delta.changes:
                fields += str("<strong>{}</strong> <span style='background-color:#ffb5ad'>{}</span>-den <span style='background-color:#b3f7ab'>{}</span>-e çalşyldy . <br/>".format(change.field, change.old, change.new))
            return format_html(fields)
        return None
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = [
        'code',
        'initial_dest',
        'final_dest',
        'payment_type',
        'initial_price',
        'service_fee',
        'final_price',
        'status',
        'in_center'
    ]
    list_filter = (
        'status',
        'payment_type',
        'initial_dest',
        'final_dest',
        'in_center',
    )

    fieldsets = (
        ('Order  Information',{
            'fields':('code','payment_type','time','service_fee','status','in_center')
        }),
        ('Payment and Delivery Details',{
            'fields':('initial_dest','final_dest')
        })
    )
    actions = [pullary_merkeze]


class CashRegisterMix(CashRegisterAdmin,CashRegisterHistoryAdmin):
    pass


admin.site.register(models.Cash_registers,CashRegisterMix)
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.Order_item)

