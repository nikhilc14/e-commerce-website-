# Generated by Django 3.2.5 on 2022-01-29 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_remove_auctions_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.categories'),
        ),
    ]
