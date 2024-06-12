from textwrap import dedent
from django.db import models
from uuid import uuid4
from django.utils.text import slugify

POST_DESCRIPTION_MAX_LENGTH = 2 * 1024 * 1024 # 2MiB
FEED_DESCRIPTION_MAX_LENGTH = 10*1024 # 10KiB

class JobState(models.TextChoices):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED  = "failed"

class FeedType(models.TextChoices):
    RSS = "rss"
    ATOM = "atom"


# Create your models here.

class SlugField(models.CharField):
    def get_prep_value(self, value):
        return slugify(str(value))

class Category(models.Model):
    name = SlugField(max_length=1000, primary_key=True)




class Feed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, help_text="UUID of feed generated by history4feed")
    title = models.CharField(max_length=1000, help_text="found in the <channel> of RSS output. Is always kept up to date with the latest feed import values for this property.")
    description = models.CharField(max_length=FEED_DESCRIPTION_MAX_LENGTH, help_text="found in the <channel> of RSS output. Is always kept up to date with the latest feed import values for this property.")
    url = models.URLField(max_length=1000, unique=True, help_text=dedent("""
        The URL of the RSS or ATOM feed

        Note this will be validated to ensure the feed is in the correct format.
    """))
    earliest_item_pubdate = models.DateTimeField(null=True, help_text="pubdate of earliest post")
    latest_item_pubdate = models.DateTimeField(null=True, help_text="pubdate of latest post")
    datetime_added = models.DateTimeField(auto_now_add=True, editable=False, help_text="date feed entry was added to database")
    feed_type = models.CharField(choices=FeedType.choices, max_length=12, null=False, editable=False, help_text="type of feed")
    retrieve_full_text = models.BooleanField(default=True, help_text="choose whether or not the server should fetch full text for this feed. default: True")

    def get_post_count(self):
        return self.posts.count()

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, help_text="UUID of job")
    state = models.CharField(choices=JobState.choices, max_length=12, default=JobState.PENDING, null=False, help_text="state of the job")
    run_datetime = models.DateTimeField(auto_now_add=True, editable=False, help_text="time job was executed")
    earliest_item_requested = models.DateTimeField(null=True, help_text="shows the earliest time for posts requested. Useful for when jobs are run to see if the time range it runs across is expected")
    latest_item_requested = models.DateTimeField(null=True, help_text="shows the latest time for posts requested")
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    info = models.CharField(max_length=FEED_DESCRIPTION_MAX_LENGTH, help_text="contains a useful summary of the job (e.g. number of posts retrieved, errors logged)")


class FullTextState(models.TextChoices):
    RETRIEVED  = "retrieved"
    SKIPPED    = "skipped"
    FAILED     = "failed"
    RETRIEVING = "retrieving"

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, help_text="UUID of items generated by history4feed")
    datetime_added = models.DateTimeField(auto_now_add=True, editable=False)
    datetime_updated = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1000, help_text="found in the <item> element of feed output")
    description = models.CharField(max_length=POST_DESCRIPTION_MAX_LENGTH, blank=True, help_text="found in the <item> element of feed output")
    link = models.URLField(max_length=1000, help_text="link to full article. found in the <item> element of feed output")
    pubdate = models.DateTimeField(help_text="date of publication.")
    author = models.CharField(max_length=1000, help_text="author of the post")
    categories = models.ManyToManyField(Category, related_name="posts", help_text="categories of the post")
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name="posts", help_text="feed id this item belongs too")
    is_full_text = models.BooleanField(default=False, help_text="if full text has been retrieved")
    content_type = models.CharField(default="plain/text", max_length=200, help_text="content type of the description")

    class  Meta:
        constraints = [
            models.UniqueConstraint(fields=["link", "feed"], name="unique_link_by_field"),
        ]

    def add_categories(self, categories):
        categories = [Category.objects.get_or_create(name=name)[0] for name in categories]
        self.categories.set(categories)

class FulltextJob(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name="fulltext_jobs", on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=FullTextState.choices, default=FullTextState.RETRIEVING)
    error_str = models.CharField(max_length=1500, null=True, blank=True)





