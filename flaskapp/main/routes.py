from flask import render_template, request, url_for, Response, redirect, flash
from flaskapp.camera import Video
from flask import Blueprint
from flask_login import login_required

main = Blueprint('main', __name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
        yield frame
        yield b'\r\n\r\n'


@main.route("/")
def home():
    return render_template('index.html')


@main.route("/about")
def about():
    return render_template('about.html')


@main.route('/video_detect', methods=['GET', 'POST'])
def video_detect():
    video = Video()
    if request.method == 'POST':
        video.close_camera()
        return redirect(url_for('main.detect'))
    return Response(gen(video),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@main.route("/detect", methods=['GET', 'POST'])
@login_required
def detect():
    if request.method == 'POST':
        return render_template('video_detect.html')
    return render_template('detect.html')


@main.route("/contact")
def contact():
    return render_template('contact.html')
