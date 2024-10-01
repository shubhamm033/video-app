from rest_framework import serializers
from django.db import transaction
from .models import Video, VideoViews, User
from datetime import datetime, timedelta


class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    email = serializers.CharField()

    def create(self, data):
        try:
            user = User.objects.create(**data)
            return user
        except Exception as e:
            raise serializers.ValidationError("Error occurred while creating users")


class VideoSerializer(serializers.Serializer):
    video_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    uploader_id = serializers.IntegerField()
    video_url = serializers.URLField()
    updated_at = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate_video_url(self, value):
        if not value.endswith(".com"):
            raise serializers.ValidationError("Invalid format")
        return value

    def create(self, data):

        try:
            with transaction.atomic():
                user = User.objects.get(user_id=data["uploader_id"])
                data["uploader"] = user
                video = Video.objects.create(**data)
                VideoViews.objects.create(video=video)
            return video
        except Exception as e:
            raise serializers.ValidationError("Error occured while creating video")


class VideoDetailsSerializer(serializers.Serializer):
    video_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    uploader_id = serializers.IntegerField()
    video_url = serializers.URLField()
    created_at = serializers.DateTimeField(read_only=True)
    view = serializers.IntegerField()

    @classmethod
    def from_instance(cls, instance):
        return cls({'video_id': instance.video_id,
                    'title': instance.title,
                    'description': instance.description,
                    'uploader_id': instance.uploader.user_id,
                    'video_url': instance.video_url,
                    'created_at': instance.created_at,
                    'view': instance.video_views.count
                    })


class WatchVideoSerializer(serializers.Serializer):
    title = serializers.CharField()
    uploader_id = serializers.IntegerField()

    def validate(self, data):

        try:
            video = Video.objects.get(title=data["title"], uploader_id=data["uploader_id"])
            data["video"] = video
        except Video.DoesNotExist:
            raise serializers.ValidationError("Video with the given uploaderId and title does not exist.")

        return data
