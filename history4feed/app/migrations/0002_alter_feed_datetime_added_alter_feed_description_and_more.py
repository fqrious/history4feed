# Generated by Django 5.0.6 on 2024-06-05 16:29

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='datetime_added',
            field=models.DateTimeField(auto_now_add=True, help_text='date feed entry was added to database'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='description',
            field=models.CharField(help_text='found in the <channel> of RSS output. Is always kept up to date with the latest feed import values for this property.', max_length=10240),
        ),
        migrations.AlterField(
            model_name='feed',
            name='earliest_item_pubdate',
            field=models.DateTimeField(help_text='pubdate of earliest post', null=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='feed_type',
            field=models.CharField(choices=[('rss', 'Rss'), ('atom', 'Atom')], editable=False, help_text='type of feed', max_length=12),
        ),
        migrations.AlterField(
            model_name='feed',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='UUID of feed generated by history4feed', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='feed',
            name='latest_item_pubdate',
            field=models.DateTimeField(help_text='pubdate of latest post', null=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='retrieve_full_text',
            field=models.BooleanField(default=True, help_text='choose whether or not the server should fetch full text for this feed. default: True'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='title',
            field=models.CharField(help_text='found in the <channel> of RSS output. Is always kept up to date with the latest feed import values for this property.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='feed',
            name='url',
            field=models.URLField(help_text='\nThe URL of the RSS or ATOM feed\n\nNote this will be validated to ensure the feed is in the correct format.\n', max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='earliest_item_requested',
            field=models.DateTimeField(help_text='shows the earliest time for posts requested. Useful for when jobs are run to see if the time range it runs across is expected', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='UUID of job', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='info',
            field=models.CharField(help_text='contains a useful summary of the job (e.g. number of posts retrieved, errors logged)', max_length=10240),
        ),
        migrations.AlterField(
            model_name='job',
            name='latest_item_requested',
            field=models.DateTimeField(help_text='shows the latest time for posts requested', null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='run_datetime',
            field=models.DateTimeField(auto_now_add=True, help_text='time job was executed'),
        ),
        migrations.AlterField(
            model_name='job',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('success', 'Success'), ('failed', 'Failed')], default='pending', help_text='state of the job', max_length=12),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(help_text='author of the post', max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(help_text='categories of the post', related_name='posts', to='app.category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(default='plain/text', help_text='content type of the description', max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(blank=True, help_text='found in the <item> element of feed output', max_length=2097152),
        ),
        migrations.AlterField(
            model_name='post',
            name='feed',
            field=models.ForeignKey(help_text='feed id this item belongs too', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='app.feed'),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='UUID of items generated by history4feed', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_full_text',
            field=models.BooleanField(default=False, help_text='if full text has been retrieved'),
        ),
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.URLField(help_text='link to full article. found in the <item> element of feed output', max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='pubdate',
            field=models.DateTimeField(help_text='date of publication.'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='found in the <item> element of feed output', max_length=1000),
        ),
    ]
