# Generated by Django 4.2.3 on 2023-08-28 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('borrowings', '0002_alter_borrowing_book_alter_borrowing_user'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='borrowing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='borrowings.borrowing'),
        ),
    ]
