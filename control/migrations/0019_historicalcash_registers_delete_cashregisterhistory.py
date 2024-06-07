# Generated by Django 4.2.13 on 2024-06-05 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('control', '0018_cashregisterhistory_delete_historicalcash_registers'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCash_registers',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Kassanyň ady')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Adress')),
                ('balance', models.FloatField(default=0, verbose_name='Balans')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Kassa',
                'verbose_name_plural': 'historical Kassalar',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.DeleteModel(
            name='CashRegisterHistory',
        ),
    ]