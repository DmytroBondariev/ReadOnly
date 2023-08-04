# Generated by Django 4.2.3 on 2023-08-04 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('borrowings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PAID', 'PAID')], max_length=10)),
                ('type', models.CharField(choices=[('PAYMENT', 'PAYMENT'), ('FINE', 'FINE')], max_length=10)),
                ('session_url', models.URLField()),
                ('session_id', models.CharField(max_length=100)),
                ('money_to_pay', models.DecimalField(decimal_places=2, max_digits=8)),
                ('borrowing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='borrowings.borrowing')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]