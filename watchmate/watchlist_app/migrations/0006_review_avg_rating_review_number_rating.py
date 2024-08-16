# Generated by Django 5.0.4 on 2024-05-01 06:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("watchlist_app", "0005_review_review_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="avg_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="review",
            name="number_rating",
            field=models.IntegerField(default=0),
        ),
    ]