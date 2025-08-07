# detection_app/views.py

from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from .utils import DetectionStream
import cv2

# ✅ Replace with fast public MJPEG stream
# STREAM_URL = "http://195.113.209.165:8080/mjpg/video.mjpg"

# # Global detection stream instance
# stream = DetectionStream(STREAM_URL)

# def live_view(request):
#     return render(request, "live.html")

# def video_feed(request):
#     if not stream.running:
#         stream.start()

#     def generate():
#         while True:
#             frame = stream.get_frame()
#             if frame is None:
#                 continue

#             ret, buffer = cv2.imencode(".jpg", frame)
#             if not ret:
#                 continue

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

#     return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace; boundary=frame")

# def stats_feed(request):
#     return JsonResponse(stream.get_stats())
import os
from django.conf import settings
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from .detection_stream import DetectionStream

# ✅ Path to your static video file (put test_vidtest_videoeo.mp4 in media folder)
VIDEO_PATH = os.path.join(settings.MEDIA_ROOT, "istockphoto-927128958-640_adpp_is.mp4")

# Global stream object
stream = DetectionStream(VIDEO_PATH)

def live_view(request):
    return render(request, "live.html")

def video_feed(request):
    if not stream.running:
        stream.start()

    def generate():
        while True:
            frame = stream.get_frame()
            if frame is None:
                continue

            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace; boundary=frame")

def stats_feed(request):
    return JsonResponse(stream.get_stats())
    def stop_stream(request):
        if stream.running:
            stream.stop()
            return JsonResponse({"status": "stopped"})
        return JsonResponse({"status": "already_stopped"})