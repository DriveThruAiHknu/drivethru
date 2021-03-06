# Generated by Django 3.1.3 on 2022-03-25 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cafe',
            fields=[
                ('manager_password', models.IntegerField(primary_key=True, serialize=False)),
                ('staff_password', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('login_id', models.IntegerField(primary_key=True, serialize=False)),
                ('password', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='member',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('member_car', models.TextField(max_length=10)),
                ('member_name', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='prod',
            fields=[
                ('prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('prod_category', models.TextField(max_length=10)),
                ('prod_name', models.TextField(max_length=20)),
                ('prod_price', models.IntegerField()),
                ('prod_image', models.ImageField(blank=True, upload_to='')),
                ('prod_recommend', models.BooleanField()),
                ('prod_hot_cold', models.IntegerField()),
                ('prod_caf_amount', models.BooleanField()),
                ('prod_syrup', models.IntegerField()),
                ('prod_shot', models.BooleanField()),
                ('prod_milk', models.BooleanField()),
                ('prod_whip', models.BooleanField()),
                ('prod_java_chip', models.BooleanField()),
                ('prod_driz', models.BooleanField()),
                ('prod_sales_rate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='today_user',
            fields=[
                ('today_user_id', models.AutoField(primary_key=True, serialize=False)),
                ('today_user_car', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='receipt',
            fields=[
                ('receipt_id', models.AutoField(primary_key=True, serialize=False)),
                ('receipt_price', models.IntegerField()),
                ('receipt_date', models.DateTimeField(auto_now_add=True)),
                ('receipt_today_id', models.IntegerField()),
                ('member_id', models.ForeignKey(db_column='memberID', on_delete=django.db.models.deletion.CASCADE, to='drive_restapi.member')),
                ('today_user_id', models.ForeignKey(db_column='todayUserID', on_delete=django.db.models.deletion.CASCADE, to='drive_restapi.today_user')),
            ],
        ),
        migrations.CreateModel(
            name='item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_quantity', models.IntegerField()),
                ('item_size', models.IntegerField()),
                ('item_price', models.IntegerField()),
                ('item_hot_cold', models.IntegerField()),
                ('item_caf_amount', models.IntegerField()),
                ('item_syrup', models.IntegerField()),
                ('item_shot', models.IntegerField()),
                ('item_milk', models.IntegerField()),
                ('item_whip', models.IntegerField()),
                ('item_java_chip', models.IntegerField()),
                ('item_driz', models.IntegerField()),
                ('prod_id', models.ForeignKey(db_column='prodID', on_delete=django.db.models.deletion.CASCADE, to='drive_restapi.prod')),
                ('receipt_id', models.ForeignKey(db_column='orderID', on_delete=django.db.models.deletion.CASCADE, to='drive_restapi.receipt')),
            ],
        ),
    ]
