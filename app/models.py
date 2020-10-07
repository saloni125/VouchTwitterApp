from django.conf import settings
from django.db import models
from django.utils import timezone


class Tweet(models.Model):
    tweet_id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=500)
    url = models.URLField()
    user_id = models.BigIntegerField()
    user_screen_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=200)
    # url_count = models.IntegerField()

    def __str__(self):
        return str(self.tweet_id) + ' == ' + self.user_name

class Domain(models.Model):
    
    class Meta:
        unique_together = (('tweet_id', 'domain_name'), )
    
    tweet_id = models.BigIntegerField()
    domain_name = models.URLField()

    def __str__(self):
        return str(self.tweet_id) + ' == ' + self.domain_name