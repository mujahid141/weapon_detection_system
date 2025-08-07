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
import os
import cv2
from django.conf import settings
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .detection_stream import DetectionStream

# Global stream object (initially None)
stream = None

def index(request):
    return render(request, "index.html")

def reports(request):
    return render(request, "reports.html")

def video_feed(request):
    global stream

    if not stream or not stream.running:
        return JsonResponse({"error": "Stream not initialized or not running"}, status=400)

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
    global stream
    if stream:
        return JsonResponse(stream.get_stats())
    return JsonResponse({"error": "Stream not running"}, status=400)

def stop_stream(request):
    global stream
    if stream and stream.running:
        stream.stop()
        return JsonResponse({"status": "stopped"})
    return JsonResponse({"status": "already_stopped"})

def upload_video(request):
    global stream
    result_video_url = None

    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']

        # Save uploaded file
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(video_file.name, video_file)
        uploaded_path = fs.path(filename)

        # Stop previous stream if running
        if stream and stream.running:
            stream.stop()

        # Create a new stream with uploaded video
        stream = DetectionStream(uploaded_path)
        stream.start()

        # You can optionally show result video URL
        result_video_url = os.path.join(settings.MEDIA_URL, 'uploads', filename)

    return render(request, "index.html", {
        'result_video': result_video_url
    })

# ✅ Path to your static video file (put test_vidtest_videoeo.mp4 in media folder)
# VIDEO_PATH = os.path.join(settings.MEDIA_ROOT, "istockphoto-927128958-640_adpp_is.mp4")
VIDEO_PATH = os.path.join(settings.MEDIA_ROOT, "Shadow of War combat is beautiful - Stealthy Enough (1080p, h264).mp4")
# VIDEO_PATH = os.path.join(settings.MEDIA_ROOT, "RAW_ #shooting caught on Lemay security #camera.mp4")

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