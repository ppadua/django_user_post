# Generated by Django 2.0.4 on 2018-04-27 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_message', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_message', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('user_level', models.IntegerField()),
                ('description', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='posted_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='poster_by', to='user_dashboard.User'),
        ),
        migrations.AddField(
            model_name='post',
            name='posted_to',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='poster_to', to='user_dashboard.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='user_dashboard.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='commentor', to='user_dashboard.User'),
        ),
    ]
