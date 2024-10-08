from django.db.models import F
from django.shortcuts import render

from rest_framework.decorators import api_view
from .serializers import VideoSerializer, WatchVideoSerializer, UserSerializer, VideoDetailsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import VideoViews, User, Video
import threading
from datetime import datetime
from django.db import transaction

lock = threading.Lock()


# Create your views here.
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user = serializer.save()
            return Response({"success": "user created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_video_details(request):
    serializer = VideoSerializer(data=request.data)

    if serializer.is_valid():
        try:
            video = serializer.save()
            return Response({"success": "video created"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def fetch_video_details(request, id):
    try:

        video = Video.objects.select_related("video_views").filter(video_id=id).first()
        serialzer = VideoDetailsSerializer.from_instance(video)

        return Response(serialzer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Not found " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def watch_video(request):
    start_time = datetime.now()
    serializer = WatchVideoSerializer(data=request.data)
    if serializer.is_valid():
        try:
            with transaction.atomic():
                video_views = VideoViews.objects.get(video=serializer.validated_data["video"])
                print("count of inventory is " + str(video_views.count))

                if video_views.count > 0:
                    video_views.count -= 1
                    video_views.save()
                else:
                    return Response({"success": "tv watching_not_allowed, all seats full",
                                     "response_time": (datetime.now() - start_time).microseconds},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "tv watching_allowed",
                             "response_time": (datetime.now() - start_time).microseconds},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
