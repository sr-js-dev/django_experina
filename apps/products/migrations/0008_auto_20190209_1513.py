# Generated by Django 2.1.5 on 2019-02-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20190209_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.Color', verbose_name='kleur'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='products', to='products.Size', verbose_name='afmeting'),
        ),
    ]