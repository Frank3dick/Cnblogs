# Generated by Django 5.1.6 on 2025-04-26 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_user_accounts_us_usernam_982a75_idx"),
        ("comments", "0002_alter_comment_create_time"),
        ("text_app", "0002_alter_article_create_time_alter_article_update_time"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["up_user_id", "article_id"],
                name="comments_co_up_user_75183a_idx",
            ),
        ),
    ]
