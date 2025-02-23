# Generated by Django 5.1.6 on 2025-02-18 10:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='موجودی به ریال')),
                ('bank_name', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionType', models.CharField(choices=[('Bank to Walet', 'Bank to Walet'), ('Walet to Walet', 'Walet to Walet')], max_length=15)),
                ('name_bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banks.bank')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='موجودی به ریال')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver_transactions', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_transactions', to=settings.AUTH_USER_MODEL)),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banks.transactiontype')),
            ],
        ),
        migrations.CreateModel(
            name='Walet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50, unique=True)),
                ('amount', models.IntegerField(verbose_name='موجودی به ریال')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transactiontype',
            name='name_walet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='banks.walet'),
        ),
    ]
