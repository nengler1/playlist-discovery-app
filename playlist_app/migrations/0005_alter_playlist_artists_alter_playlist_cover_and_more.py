# Generated by Django 4.2 on 2024-04-06 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist_app', '0004_artist_genre_remove_playlist_artists_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='artists',
            field=models.ManyToManyField(default=None, to='playlist_app.artist'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='cover',
            field=models.ImageField(null=True, upload_to='static/uploads/'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='genres',
            field=models.ManyToManyField(default=None, to='playlist_app.genre'),
        ),
    ]
