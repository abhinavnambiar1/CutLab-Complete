from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, send_file
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/upload'
app.config['EDITED_FOLDER'] = './static/edited'


@app.route('/')
def main_page():
    return render_template('index.html')


ALLOWED_EXTENSIONS = ['mp4']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/workspace')
def workspace():
    return render_template('workspace.html')

@app.route('/trim', methods=['GET', 'POST'])
def trimvideo():
    return render_template('trim.html')

ALLOWED_EXTENSIONS = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'mpeg', 'mpg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# Trim Videos Part 



@app.route('/uploadtrim', methods=['POST'])
def uploadtrim():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_trim.html', video_filename_trim=video.filename)
    return "Invalid File Type"

@app.route('/finaltrim', methods=['GET','POST'])
def trim_video():
    video_filename_trim = request.form['video_filename_trim']
    start_time = float(request.form['start_time'])
    end_time = float(request.form['end_time']) 

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_trim}"
    edited_folder = app.config['EDITED_FOLDER']
    
    # Create the edited folder if it doesn't exist
    # if not os.path.exists(edited_folder):
    #     os.makedirs(edited_folder)

    trimmed_video_filename = f"trimmed_{video_filename_trim}"
    trimmed_video_path = os.path.join(edited_folder, trimmed_video_filename)

    video1 = VideoFileClip(original_video_path)
    trimmed_video = video1.subclip(start_time, end_time)
    trimmed_video.write_videofile(trimmed_video_path, codec="libx264", audio_codec="aac")

    return render_template('trim_final.html', video_path=trimmed_video_filename, os=os)

@app.route('/download/<filename>')
def download_trim(filename):
    # Use url_for to generate the correct URL for the edited folder
    edited_folder = app.config['EDITED_FOLDER']
    return send_file(os.path.join(edited_folder, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=3050)

