# Generated by Django 5.0.6 on 2024-05-24 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0007_order_item_final_dest_order_item_initial_dest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Sargyt', 'verbose_name_plural': 'Sargytlar'},
        ),
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(default='1', max_length=50, verbose_name='Sargydyň kody'),
        ),
        migrations.AlterField(
            model_name='order',
            name='final_dest',
            field=models.CharField(choices=[('J', 'Jemlenýär'), ('M', 'Mary'), ('A', 'Aşgabat'), ('L', 'Lebap'), ('D', 'Daşoguz'), ('B', 'Balkan')], max_length=50, verbose_name='Sargydyň barmaly ýeri'),
        ),
        migrations.AlterField(
            model_name='order',
            name='final_price',
            field=models.FloatField(blank=True, max_length=50, null=True, verbose_name='Müşderiniň töläni'),
        ),
        migrations.AlterField(
            model_name='order',
            name='in_center',
            field=models.BooleanField(default=False, verbose_name='Pul merkezdemi?'),
        ),
        migrations.AlterField(
            model_name='order',
            name='initial_dest',
            field=models.CharField(choices=[('J', 'Jemlenýär'), ('M', 'Mary'), ('A', 'Aşgabat'), ('L', 'Lebap'), ('D', 'Daşoguz'), ('B', 'Balkan')], default='J', max_length=50, verbose_name='Şu wagtky ýerleşýän ýeri'),
        ),
        migrations.AlterField(
            model_name='order',
            name='initial_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('N', 'Nagt'), ('C', 'Terminal'), ('O', 'Online'), ('K', 'Karz')], default='N', max_length=50, verbose_name='Tölegiň görnüşi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='service_fee',
            field=models.FloatField(blank=True, max_length=50, null=True, verbose_name='Hyzmatyň bahasy'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', '📦'), ('D', '❌'), ('H', '❕'), ('S', '✅')], default='P', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Sargyt edilen wagty'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='barcode',
            field=models.CharField(max_length=50, verbose_name='Harydyň kody'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='final_dest',
            field=models.CharField(choices=[('J', 'Jemlenýär'), ('M', 'Mary'), ('A', 'Aşgabat'), ('L', 'Lebap'), ('D', 'Daşoguz'), ('B', 'Balkan')], max_length=50, verbose_name='Harydyň jemlenýän ýeri'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='final_quantity',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Harydyň kabul edilen mukdary'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='initial_dest',
            field=models.CharField(choices=[('J', 'Jemlenýär'), ('M', 'Mary'), ('A', 'Aşgabat'), ('L', 'Lebap'), ('D', 'Daşoguz'), ('B', 'Balkan')], max_length=50, verbose_name='Harydyň ýerleşýän ýeri'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='initial_quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Harydyň mukdary'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='item_price',
            field=models.FloatField(help_text='Harydyň bahasy'),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Harydyň razmeri, ýok bolsa boş'),
        ),
    ]
