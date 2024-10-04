from django.db import models
from datetime import timezone, datetime
from django.core.exceptions import ValidationError
import time

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField()
    updated_at = models.DateTimeField(default=datetime.now())
    created_at = models.DateTimeField(default=datetime.now())


class VideoViews(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='video_views')
    count = models.IntegerField(default=0)
    version = models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        if self.pk:
            # time.sleep(2)
            current_version = VideoViews.objects.get(pk=self.pk).version
            print(current_version, self.version)
            if self.version != current_version:
                raise ValidationError("Some other transcation updated it, versionchanges")

            self.version += 1
        super(VideoViews, self).save(*args, **kwargs)
