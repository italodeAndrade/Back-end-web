# Generated by Django 5.1.2 on 2024-10-28 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmes', '0001_initial'),
        ('users', '0006_remove_cliente_senha_cliente_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filme',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.cliente'),
        ),
    ]
