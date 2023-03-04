# Generated by Django 2.2.28 on 2023-03-04 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thepetproject', '0002_auto_20230303_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHasLikedPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thepetproject.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thepetproject.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserHasLikedComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thepetproject.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thepetproject.UserProfile')),
            ],
        ),
    ]
