# Generated by Django 4.2.3 on 2023-07-28 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_remove_book_inventory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title', 'author', 'cover']},
        ),
    ]