# Generated by Django 5.1.6 on 2025-02-18 10:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0003_alter_transactiontype_name_bank_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionreceipt',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipt', to='banks.transaction'),
        ),
    ]
