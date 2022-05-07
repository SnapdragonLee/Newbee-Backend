# Generated by Django 3.2 on 2022-05-07 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0002_auto_20220507_2118'),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=50, verbose_name='用户的openid')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.question', verbose_name='对应的问题')),
            ],
        ),
    ]