from flask import Flask, render_template, request, redirect
from licence_detector import *
from extractor_tessaract import *
from database_handler import *

app = Flask(__name__,
            static_url_path='',
            static_folder='views/static',
            template_folder='views/templates')


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/show')
def show():
    data = get_all_data()
    return render_template("show.html", data=data)


@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return render_template("home.html", errorMsg="No video file found!!")
    video = request.files['video']
    if video.filename == "":
        return render_template("home.html", errorMsg='No video file selected!!')
    extension = video.filename.split(".")[1]
    # saving for backend use
    try:
        video.save("upload/output"+"."+extension)
    except Exception as e:
        print(str(e))
        return render_template("home.html", errorMsg="Unable to upload!!")
    # Detecting vehicals from video
    try:
        detector = Detector()
        detector.process()
    except Exception as e:
        print(str(e))
        return render_template("home.html", errorMsg="Unable to detect vehicles from video!!")
    # Extracting licence plate from vehicals
    plate_details = None
    try:
        plate_details = extract_number_plate()
    except Exception as e:
        print(str(e))
        return render_template("home.html", errorMsg="Failed to detect number plates!!")
    # store in database
    try:
        append_details(plate_details)
    except Exception as e:
        print(str(e))
        return render_template("home.html", errorMsg="Failed to save in Database!!")
    return redirect("/show")


@app.route('/api/image/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('upload/images/', filename+'.png')


if __name__ == '__main__':
    app.run(port=2000)
