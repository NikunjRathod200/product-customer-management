# Generated by Django 3.2.3 on 2021-09-19 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_companyproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tot_price', models.PositiveIntegerField(default=0)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('order_dt', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(default=False, max_length=20)),
                ('comp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.company')),
                ('cust', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.companycustomer')),
                ('prod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.companyproduct')),
            ],
        ),
    ]