# Generated by Django 5.1.6 on 2025-04-18 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_group_psychologicalportrait_representationalsystem_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trait', models.CharField(max_length=255)),
                ('min_score', models.IntegerField()),
                ('max_score', models.IntegerField()),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scales', to='core.test')),
            ],
        ),
    ]
