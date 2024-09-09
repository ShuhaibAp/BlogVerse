# Generated by Django 5.1 on 2024-09-09 09:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_username_alter_blog_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Bio',
            new_name='bio',
        ),
        migrations.AddField(
            model_name='blog',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='blog_bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='blog_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('Technology', 'Technology'), ('Business', 'Business'), ('Anime', 'Anime'), ('Cars', 'Cars'), ('Story', 'Story'), ('Food', 'Food'), ('Sports', 'Sports')], default='Technology', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
