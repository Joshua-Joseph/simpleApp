from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
import cv2
from PIL import Image
from pancard.ocr import ocr_space_file
import json

# Create your views here.
capture = 1


def result(request):
    try:
        parsedText = ocr_space_file('/Users/joshua/Desktop/internship/PanCard.png')
        parsedText = json.loads(parsedText)
        text = parsedText['ParsedResults'][0]['ParsedText']
        text = text.split('\n')
    except:
        text = ['Not able to process the Image. Try again']
    return render(request, 'pancard/res.html', context={'text': text})


def homepage(request):
    global capture
    if(request.method == 'GET'):
        capture = 1
        return render(request, 'pancard/home.html')
    if(request.method == 'POST'):
        click = request.POST.get('click')
        if click is not None:
            capture = 0
        return redirect('res')


def gen():
    global capture
    camera = cv2.VideoCapture(0)
    while capture:
        success, frame = camera.read()
        if success:
            frame_flip = cv2.flip(frame, 1)
            ret, jpeg = cv2.imencode('.jpg', frame_flip)
            if(capture == 0):
                cv2.imwrite('PanCard.png', frame)
                img = Image.open('PanCard.png')
                img = img.resize((960, 640), Image.ANTIALIAS)
                img.save('PanCard.png', optimize=True, quality=50)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# Method for laptop camera


def video_feed(request):
    return StreamingHttpResponse(gen(),
                                 # video type
                                 content_type='multipart/x-mixed-replace; boundary=frame')
