from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, send_file
from moviepy.editor import VideoFileClip, vfx, concatenate_videoclips, AudioFileClip, ImageClip, CompositeVideoClip, TextClip
import os
from werkzeug.utils import secure_filename

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

ALLOWED_EXTENSIONS = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'mpeg', 'mpg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# Trim Videos Part 

@app.route('/trim', methods=['GET', 'POST'])
def trimvideo():
    return render_template('trim.html')

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

# Black and White Videos Part
@app.route('/blackwhite', methods=['GET', 'POST'])
def blackwhitevideo():
    return render_template('blackwhite.html')

@app.route('/uploadblackwhite', methods=['POST'])
def uploadblackwhite():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_blackwhite.html', video_filename_blackwhite=video.filename)
    return "Invalid File Type"

@app.route('/finalblackwhite', methods=['GET','POST'])
def blackwhite_video():
    video_filename_blackwhite = request.form['video_filename_blackwhite']

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_blackwhite}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    blackwhited_video_filename = f"blackwhited_{video_filename_blackwhite}"
    blackwhited_video_path = os.path.join(edited_folder, blackwhited_video_filename)

    video1 = VideoFileClip(original_video_path)
    blackwhited_video = video1.fx(vfx.blackwhite)
    blackwhited_video.write_videofile(blackwhited_video_path, codec="libx264", audio_codec="aac")

    return render_template('blackwhite_final.html', video_path1=blackwhited_video_filename, os=os)


# Merge Videos Part
@app.route('/mergevideos', methods=['GET','POST'])
def mergevidvideo():
    return render_template('mergevid.html')

@app.route('/uploadmergevid', methods=['POST'])
def uploadmergevid():
    # Check if the request contains 'video1' and 'video2'
    if 'video1' not in request.files or 'video2' not in request.files:
        return "Two video files are required"

    video1 = request.files['video1']
    video2 = request.files['video2']

    # Check if video1 is empty
    if video1.filename == "":
        return "No video file selected for the first video"

    # Check if video2 is empty
    if video2.filename == "":
        return "No video file selected for the second video"

    # Check if both files have allowed extensions
    if video1 and allowed_file(video1.filename) and video2 and allowed_file(video2.filename):
        # Save the uploaded videos
        video1.save('./static/upload/' + video1.filename)
        video2.save('./static/upload/' + video2.filename)

        return render_template('preview_mergevid.html', 
                               video1_file=video1.filename,
                               video2_file=video2.filename)
    return "Invalid File Type for one or both videos"

def merge_videos(video1_path, video2_path):
    clip1 = VideoFileClip(video1_path)
    clip2 = VideoFileClip(video2_path)

    # Ensure both clips have the same duration
    # duration = min(clip1.duration, clip2.duration)
    # clip1 = clip1.subclip(0, duration)
    # clip2 = clip2.subclip(0, duration)

    # Concatenate video clips
    merged_clip = concatenate_videoclips([clip1, clip2])

    return merged_clip


@app.route('/finalmergevid', methods=['GET','POST'])
def mergevid_video():
    video1_file = request.form['video1_file']
    video2_file = request.form['video2_file']

    # original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video1_file, video2_file}"
    edited_folder = app.config['EDITED_FOLDER']

    merged_video_filename = f"merged_{video1_file}"
    merged_video_path = os.path.join(edited_folder, merged_video_filename)

    if video1_file and video2_file:
        # Save the uploaded videos
        video1_path = os.path.join(app.config['UPLOAD_FOLDER'], video1_file)
        video2_path = os.path.join(app.config['UPLOAD_FOLDER'], video2_file)

        # video1_file.save(video1_path)
        # video2_file.save(video2_path)

        # shutil.copy(video1_file.filename, video1_path)
        # shutil.copy(video2_file.filename, video2_path)

        # Merge videos
        # video3 = VideoFileClip(original_video_path)
        merged_video = merge_videos(video1_path, video2_path)

        # Save merged video
        # output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged_video.mp4')
        merged_video.write_videofile(merged_video_path, codec='libx264', audio_codec='aac')

        return render_template('mergevid_final.html', video_path=merged_video_filename, os=os)

# Add Music Part
@app.route('/addmusic', methods=['GET','POST'])
def addmusicvideo():
    return render_template('addmusic.html')

@app.route('/uploadaddmusic', methods=['POST'])
def uploadaddmusic():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        print(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_addmusic.html', video_filename_addmusic=video.filename)
    return "Invalid File Type"

@app.route('/finaladdmusic', methods=['GET','POST'])
def addmusic_video():
    video_filename_addmusic = request.form['video_filename_addmusic']
    audio_filename_addmusic = request.files['audio_filename_addmusic']
    
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_addmusic}"
    original_audio_path = f"{app.config['UPLOAD_FOLDER']}/{audio_filename_addmusic}"

# 
    musicadded_video_filename = f"musicadded_{video_filename_addmusic}"
    musicadded_video_path = f"{app.config['EDITED_FOLDER']}/{musicadded_video_filename}"

    if video_filename_addmusic and audio_filename_addmusic:
        original_video_path = f'{app.config["UPLOAD_FOLDER"]}/{video_filename_addmusic}'
    
        audio_filename = secure_filename(audio_filename_addmusic.filename)
        original_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        audio_filename_addmusic.save(original_audio_path)
        
        video1 = VideoFileClip(original_video_path)
        music1 = AudioFileClip(original_audio_path)
        musicadded_video = video1.set_audio(music1)
        print(musicadded_video)
        musicadded_video.write_videofile(musicadded_video_path, codec="libx264", audio_codec="aac")    
        
        return render_template('addmusic_final.html', video_path=musicadded_video_filename, os=os)

# Adjust Volume Part
@app.route('/adjustvolume', methods=['GET','POST'])
def adjustvolumevideo():
    return render_template('adjustvolume.html')

@app.route('/uploadadjustvolume', methods=['POST'])
def uploadadjustvolume():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_adjustvolume.html', video_filename_adjustvolume=video.filename)
    return "Invalid File Type"

# def adjust_audio(video_path, output_path, volume_percentage):
#     video_clip = VideoFileClip(video_path)
    
#     # Adjust the audio volume based on the user-selected factor
#     audio_clip = video_clip.audio
#     audio_clip = audio_clip.volumex(volume_percentage)
    
#     # Apply the modified audio to the video clip
#     video_clip = video_clip.set_audio(audio_clip)
    
#     # Write the modified video to the output path
#     video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

@app.route('/finaladjustvolume', methods=['GET','POST'])
def adjustvolume_video():
    video_filename_adjustvolume = request.form['video_filename_adjustvolume']
    volume_percentage = float(request.form['volume_percentage'])

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_adjustvolume}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    volumeadjusted_video_filename = f"volumeadjusted_{video_filename_adjustvolume}"
    volumeadjusted_video_path = os.path.join(edited_folder, volumeadjusted_video_filename)

    video1 = VideoFileClip(original_video_path)
    default_audio_factor = 0.5
    video1.audio.volumex(default_audio_factor)
    # volumeadjusted_video = video1.subclip(start_time, end_time)
    # Adjust the audio volume based on the user-selected factor
    output_audio = video1.audio
    output_audio = output_audio.volumex(volume_percentage)
    
    # Apply the modified audio to the video clip
    volumeadjusted_video = video1.set_audio(output_audio)
    
    # Write the modified video to the output path
    volumeadjusted_video.write_videofile(volumeadjusted_video_path, codec="libx264", audio_codec="aac")

    return render_template('adjustvolume_final.html', video_path=volumeadjusted_video_filename, os=os)

# Flip Videos Part
@app.route('/flipvideos', methods=['GET','POST'])
def flipvideo():
    return render_template('flip.html')

@app.route('/uploadflip', methods=['POST'])
def uploadflip():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_flip.html', video_filename_flip=video.filename)
    return "Invalid File Type"

@app.route('/finalflip', methods=['GET','POST'])
def flip_video():
    video_filename_flip = request.form['video_filename_flip']
    # start_time = float(request.form['start_time'])
    # end_time = float(request.form['end_time'])

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_flip}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    flipped_video_filename = f"flipped_{video_filename_flip}"
    flipped_video_path = os.path.join(edited_folder, flipped_video_filename)

    video1 = VideoFileClip(original_video_path)
    flipped_video = video1.fx(vfx.mirror_x)
    flipped_video.write_videofile(flipped_video_path, codec="libx264", audio_codec="aac")

    return render_template('flip_final.html', video_path=flipped_video_filename, os=os)

# Cut-out Videos Part
@app.route('/cutoutvideos', methods=['GET','POST'])
def cutoutvideo():
    return render_template('cutout.html')

@app.route('/uploadcutout', methods=['POST'])
def uploadcutout():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_cutout.html', video_filename_cutout=video.filename)
    return "Invalid File Type"

def cutout_unwanted_video(video_path, cutout_start, cutout_end):
    # max_duration = 3600
    # clip = VideoFileClip(video_path, max_duration=max_duration)
    clip = VideoFileClip(video_path)

    edited_clip = clip.cutout(cutout_start, cutout_end)
    # edited_clip.write_videofile(output_path,codec="libx264", audio_codec="aac")

    return edited_clip

@app.route('/finalcutout', methods=['GET','POST'])
def cutout_video():
    video_filename_cutout = request.form['video_filename_cutout']
    cutout_start = float(request.form['cutout_start'])
    cutout_end = float(request.form['cutout_end'])

    original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename_cutout)
    # original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_cutout}"
    edited_folder = app.config['EDITED_FOLDER']
 
    cutouted_video_filename = f"cutouted_{video_filename_cutout}"
    cutouted_video_path = os.path.join(edited_folder, cutouted_video_filename)

#     ffmpeg_params = [
#     '-preset', 'medium',
#     '-b:v', '2000k',
#     '-maxrate', '2500k',
#     '-bufsize', '5000k',
#     '-vf', 'scale=-1:720',
#     '-threads', '0',
#     '-tune', 'zerolatency',
#     '-crf', '23',
#     '-b:a', '192k',
#     '-strict', 'experimental'
# ]

    # video4 = VideoFileClip(original_video_path)
    cutouted_video = cutout_unwanted_video(original_video_path, cutout_start, cutout_end)
    # cutouted_video.write_videofile(cutouted_video_path, codec="libx264", audio_codec="mp3", ffmpeg_params=ffmpeg_params)
    cutouted_video.write_videofile(cutouted_video_path, codec="libx264", audio_codec="mp3")

    return render_template('cutout_final.html', video_path=cutouted_video_filename, os=os)

# Overlay Images over Videos Part
@app.route('/imagesoverlay', methods=['GET','POST'])
def overlayvideo():
    return render_template('overlay.html')

@app.route('/uploadoverlay', methods=['POST'])
def uploadoverlay():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_overlay.html', video_filename_overlay=video.filename)
    return "Invalid File Type"

# from moviepy.editor import *
# main_clip = VideoFileClip("./assets/sample3.mp4")
# overlay_image = ImageClip("./assets/image1.png")
# overlay_width = 200
# overlay_height = 150
# overlay_image = overlay_image.resize(width=overlay_width, height=overlay_height)
# overlay_opacity = 0.5
# overlay_image = overlay_image.set_opacity(overlay_opacity)
# overlay_duration = 5
# overlay_position = ("center", "center")
# overlay_clip = overlay_image.set_position(overlay_position).set_duration(overlay_duration)
# final_clip = CompositeVideoClip([main_clip, overlay_clip.set_start(10)])  
# final_clip.write_videofile("./assets/imageovervideo.mp4")

# def overlaying_image(input_path, output_path, image_path, image_width, image_height, image_opacity, image_duration, image_position_x, image_position_y, start_time):

#     # Load the main video clip
#     main_clip = VideoFileClip(input_path)

#     # Load the image to overlay
#     # image_path = f"{app.config['UPLOAD_FOLDER']}"
#     overlay_image = ImageClip(image_path)

#     # Set the width and height for the overlay image
#     overlay_width = image_width  # Adjust this as needed
#     overlay_height = image_height  # Adjust this as needed

#     # Resize the overlay image
#     overlay_image = overlay_image.resize(width=overlay_width, height=overlay_height)

#     # Set the transparency of the overlay image (0 = fully transparent, 1 = fully opaque)
#     overlay_opacity = image_opacity  # Adjust this as needed

#     # Set the opacity of the overlay image
#     overlay_image = overlay_image.set_opacity(overlay_opacity)

#     # Set the duration for which the overlay should appear (in seconds)
#     overlay_duration = image_duration  # Adjust this as needed

#     # Set the position of the overlay image
#     overlay_position = (image_position_x, image_position_y)  # You can also use pixel coordinates

#     # Set the position and duration of the overlay clip
#     overlay_clip = overlay_image.set_position(overlay_position).set_duration(overlay_duration)

#     # Overlay the clips
#     final_clip = CompositeVideoClip([main_clip, overlay_clip.set_start(start_time)])  # Set the start time for overlay

#     # Write the result to a file
#     final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close the clips
    # main_clip.close()
    # final_clip.close()

@app.route('/finaloverlay', methods=['GET','POST'])
def overlay_video():
    video_filename_overlay = request.form['video_filename_overlay']
    overlay_image = request.files['overlay_image']
    image_width = int(request.form['image_width'])
    image_height = int(request.form['image_height'])
    image_opacity = float(request.form['image_opacity'])
    image_duration = int(request.form['image_duration'])
    start_time = int(request.form['start_time'])
    image_position_x = request.form['image_position_x']
    image_position_y = request.form['image_position_y']

    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_overlay}"
    original_image_path = f"{app.config['UPLOAD_FOLDER']}/{overlay_image}"
    # print(original_image_path) 
    # edited_folder = app.config['EDITED_FOLDER']

    overlayed_video_filename = f"image_overlayed_{video_filename_overlay}"
    # overlayed_video_path = os.path.join(edited_folder, overlayed_video_filename)
    overlayed_video_path = f"{app.config['EDITED_FOLDER']}/{overlayed_video_filename}"

    if video_filename_overlay and overlay_image:
        original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_overlay}"

        image_filename = secure_filename(overlay_image.filename)
        original_image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        overlay_image.save(original_image_path)

        main_clip = VideoFileClip(original_video_path)
        # Load the image to overlay
        # image_path = f"{app.config['UPLOAD_FOLDER']}"
        overlay_image = ImageClip(original_image_path)

        # Set the width and height for the overlay image
        overlay_width = image_width  # Adjust this as needed
        overlay_height = image_height  # Adjust this as needed

        # Resize the overlay image
        overlay_image = overlay_image.resize(width=overlay_width, height=overlay_height)

        # Set the transparency of the overlay image (0 = fully transparent, 1 = fully opaque)
        overlay_opacity = image_opacity  # Adjust this as needed

        # Set the opacity of the overlay image
        overlay_image = overlay_image.set_opacity(overlay_opacity)

        # Set the duration for which the overlay should appear (in seconds)
        overlay_duration = image_duration  # Adjust this as needed

        # Set the position of the overlay image
        overlay_position = (image_position_x, image_position_y)  # You can also use pixel coordinates

        # Set the position and duration of the overlay clip
        overlay_clip = overlay_image.set_position(overlay_position).set_duration(overlay_duration)

        # Overlay the clips
        final_clip = CompositeVideoClip([main_clip,    overlay_clip.set_start(start_time)])  # Set the start time for overlay

        # Write the result to a file
        final_clip.write_videofile(overlayed_video_path, codec="libx264", audio_codec="aac")

        # overlaying_image(original_video_path,     overlayed_video_path, original_image_path, image_width, image_height, image_opacity, image_duration, image_position_x, image_position_y, start_time)
        # video1 = VideoFileClip(original_video_path)
        # overlayed_video.write_videofile(overlayed_video_path, codec="libx264", audio_codec="aac")

        return render_template('overlay_final.html', video_path=overlayed_video_filename, os=os)


# Creating GIF Parts
@app.route('/videotogif', methods=['GET','POST'])
def gifvideo():
    return render_template('gif.html')

@app.route('/uploadgif', methods=['POST'])
def uploadgif():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_gif.html', video_filename_gif=video.filename)
    return "Invalid File Type"

@app.route('/finalgif', methods=['GET','POST'])
def gif_video():
    video_filename_gif = request.form['video_filename_gif']
    timestamp = float(request.form.get('timestamp'))
    duration = float(request.form.get('duration'))

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_gif}"
    edited_folder = app.config['EDITED_FOLDER']

    # gifed_video_filename = f"gifed_{video_filename_gif}"
    gifed_video_filename = f"gifed_{os.path.splitext(video_filename_gif)[0]}" + ".gif"

    gifed_video_path = os.path.join(edited_folder, gifed_video_filename)
    # try:
    video_clip = VideoFileClip(original_video_path)
    start_time = timestamp
    end_time = timestamp + duration
    final_gif = video_clip.subclip(start_time, end_time)

    # gif_path = os.path.splitext(output_path)[0] + ".gif"
    # video_clip = VideoFileClip(original_video_path).subclip(timestamp, duration)
    # text_clip = TextClip(duration)
    # final_gif = CompositeVideoClip([video_clip, text_screeclip])
    final_gif.write_gif(gifed_video_path)

    return render_template('gif_final.html', video_path=gifed_video_filename, os=os)

# Adding Text to Videos Part
@app.route('/addtext', methods=['GET','POST'])
def addtextvideo():
    return render_template('addtext.html')

@app.route('/uploadaddtext', methods=['POST'])
def uploadaddtext():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_addtext.html', video_filename_addtext=video.filename)
    return "Invalid File Type"

# def create_text_clip(text, fontsize, color, position, duration):

#     text_clip = TextClip(text, fontsize=fontsize, color=color)
        
#     if position == 'top':
#         text_clip = text_clip.set_position(("center", "top"))
#     elif position == 'bottom':
#         text_clip = text_clip.set_position(("center", "bottom"))
#     else:
#         text_clip = text_clip.set_position("center")

#     text_clip = text_clip.set_duration(duration)
#     return text_clip

def create_text_clip(text, fontsize, color, position, duration):
    text_clip = TextClip(text, fontsize=fontsize, color=color)

    if position == 'top':
        text_clip = text_clip.set_position(("center", "top"))
    elif position == 'bottom':
        text_clip = text_clip.set_position(("center", "bottom"))
    else:
        text_clip = text_clip.set_position("center")

    text_clip = text_clip.set_duration(duration)
    return text_clip


# def addingtext(input_path, output_path, text, fontsize, color, position, duration):
def addingtext(input_path, output_path, text, fontsize, color, position, duration):

    # clip = VideoFileClip(input_path).subclip(0,20)
    clip = VideoFileClip(input_path)
    # clip = clip.subclip(text_start_time, text_end_time)
    text = TextClip(text, fontsize=fontsize, color=color)
    text = text.set_position(position).set_duration(duration)
    video = CompositeVideoClip([clip, text])
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # video = CompositeVideoClip([clip,text])
    # video.write_videofile(output_path)

@app.route('/finaladdtext', methods=['GET','POST'])
def addtext_video():
    video_filename_addtext = request.form['video_filename_addtext']
    # start_time = float(request.form['start_time'])
    # end_time = float(request.form['end_time'])
    text = request.form.get('text')
    fontsize = int(request.form.get('fontsize'))
    color = request.form.get('color', 'white')
    position = request.form.get('position')
    duration = float(request.form.get('duration'))

    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_addtext}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    text_added_video_filename = f"text_added_{video_filename_addtext}"
    text_added_video_path = os.path.join(edited_folder, text_added_video_filename)

    addingtext(original_video_path , text_added_video_path, text, fontsize, color, position, duration)

    return render_template('addtext_final.html', video_path=text_added_video_filename, os=os)

# Mute Videos
@app.route('/mutevideos', methods=['GET','POST'])
def mutevideo():
    return render_template('mute.html')

@app.route('/uploadmute', methods=['POST'])
def uploadmute():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_mute.html', video_filename_mute=video.filename)
    return "Invalid File Type"

# def mute(input_path, output_path):
#     video_clip = VideoFileClip(input_path)
#     muted_clip = video_clip.volumex(0.0)  # Mute the audio
#     muted_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
#     video_clip.close()
#     muted_clip.close()

@app.route('/finalmute', methods=['GET','POST'])
def mute_video():
    video_filename_mute = request.form['video_filename_mute']

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_mute}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    muted_video_filename = f"muted_{video_filename_mute}"
    muted_video_path = os.path.join(edited_folder, muted_video_filename)

    video1 = VideoFileClip(original_video_path)
    muted_video = video1.set_audio(None)
    muted_video.write_videofile(muted_video_path, codec="libx264", audio_codec="aac")

    return render_template('mute_final.html', video_path=muted_video_filename, os=os)

# Rotate Videos Part
@app.route('/rotatevideos', methods=['GET','POST'])
def rotatevideo():
    return render_template('rotate.html')

@app.route('/uploadrotate', methods=['POST'])
def uploadrotate():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_rotate.html', video_filename_rotate=video.filename)
    return "Invalid File Type"

@app.route('/finalrotate', methods=['GET','POST'])
def rotate_video():
    video_filename_rotate = request.form['video_filename_rotate']
    rotate_angle = float(request.form['rotate_angle'])

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_rotate}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    rotated_video_filename = f"rotated_{video_filename_rotate}"
    rotated_video_path = os.path.join(edited_folder, rotated_video_filename)

    video1 = VideoFileClip(original_video_path)
    rotated_video = video1.rotate(rotate_angle)
    rotated_video.write_videofile(rotated_video_path, codec="libx264", audio_codec="aac")

    return render_template('rotate_final.html', video_path=rotated_video_filename, os=os)

# Crop Videos Part
@app.route('/cropvideos', methods=['GET', 'POST'])
def cropvideo():
    return render_template('crop.html')

@app.route('/uploadcrop', methods=['POST'])
def uploadcrop():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_crop.html', video_filename_crop=video.filename)
    return "Invalid File Type"

def cropping_video(input_path, output_path, clicked_aspect_ratio):
    video_clip = VideoFileClip(input_path)
    if clicked_aspect_ratio == "1:1":
        # x1, y1, x2, y2 = 0, 0, 1080, 1080
        x1 = 0
        y1 = 0
        x2 = 720
        y2 = 720
        cropped_clip = video_clip.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    elif clicked_aspect_ratio == "2:3":
        # x1, y1, x2, y2 = 0, 0, 720, 1080
        x1 = 0
        y1 = 0
        x2 = 480
        y2 = 720
        cropped_clip = video_clip.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    elif clicked_aspect_ratio == "3:2":
        # x1, y1, x2, y2 = 0, 0, 720, 1080
        x1 = 0
        y1 = 0
        x2 = 720
        y2 = 480
        cropped_clip = video_clip.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    elif clicked_aspect_ratio == "4:5":
        # x1, y1, x2, y2 = 0, 0, 864, 1080
        x1 = 0
        y1 = 0
        x2 = 576
        y2 = 720
        cropped_clip = video_clip.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    elif clicked_aspect_ratio == "9:16":
        # x1, y1, x2, y2 = 0, 0, 608, 1080
        x1 = 0
        y1 = 0
        x2 = 405
        y2 = 720
        cropped_clip = video_clip.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    elif clicked_aspect_ratio == "16:9":
        # x1, y1, x2, y2 = 0, 0, 1920, 1080
        x1 = 0
        y1 = 0
        x2 = 720
        y2 = 405
        cropped_clip = video_clip.crop(x1=x1, x2=x2, y1=y1, y2=y2)

    # cropped_clip = video_clip.crop(x1=x1, x2=x2, y1=y1, y2=y2)
    cropped_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    # cropped_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp.m4a', remove_temp=True)

@app.route('/finalcrop', methods=['GET','POST'])
def crop_video():
    video_filename_crop = request.form['video_filename_crop']
    aspect_ratio = request.form['aspect_ratio']

    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_crop}"
    edited_folder = app.config['EDITED_FOLDER']

    cropped_video_filename = f"cropped_{video_filename_crop}"
    cropped_video_path = os.path.join(edited_folder, cropped_video_filename)
    # cropped_video_path = f"app.config['EDITED_FOLDER']/{cropped_video_filename}"

    cropping_video(original_video_path, cropped_video_path, aspect_ratio)

    return render_template('crop_final.html', video_path=cropped_video_filename, os=os)


# Split Videos Part
@app.route('/splitscreen', methods=['GET','POST'])
def splitvideo():
    return render_template('split.html')

@app.route('/uploadsplit', methods=['POST'])
def uploadsplit():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_split.html', video_filename_split=video.filename)
    return "Invalid File Type"

@app.route('/finalsplit', methods=['GET','POST'])
def split_video():
    video_filename_split = request.form['video_filename_split']
    split_time = float(request.form['split_time'])

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_split}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    splitted_video_filename1 = f"splitted1_{video_filename_split}"
    splitted_video_filename2 = f"splitted2_{video_filename_split}"
    splitted_video_path1 = os.path.join(edited_folder, splitted_video_filename1)
    splitted_video_path2 = os.path.join(edited_folder, splitted_video_filename2)

    video_clip = VideoFileClip(original_video_path)
    video1 = video_clip.subclip(0, split_time)
    video2 = video_clip.subclip(split_time, video_clip.duration)
    video1.write_videofile(splitted_video_path1, codec="libx264", audio_codec="aac")
    video2.write_videofile(splitted_video_path2, codec="libx264", audio_codec="aac")

    return render_template('split_final.html', video_path1=splitted_video_filename1,video_path2=splitted_video_filename2, os=os)


# Saving Frames Part
@app.route('/savingscreenshots', methods=['GET','POST'])
def screenshotvideo():
    return render_template('screenshot.html')

@app.route('/uploadscreenshot', methods=['POST'])
def uploadscreenshot():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_screenshot.html', video_filename_screenshot=video.filename)
    return "Invalid File Type"

@app.route('/finalscreenshot', methods=['GET','POST'])
def screenshot_video():
    video_filename_screenshot = request.form['video_filename_screenshot']
    time_stamp = float(request.form['time_stamp'])

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_screenshot}"
    edited_folder = app.config['EDITED_FOLDER']
# 
    screenshotted_video_filename = f"screenshotted_{os.path.splitext(video_filename_screenshot)}" + ".jpg"
    screenshotted_video_path = os.path.join(edited_folder, screenshotted_video_filename)

    video1 = VideoFileClip(original_video_path)
    # final_screenshot = video1.save_frame(screenshotted_video_path, time_stamp)
    video1.save_frame((screenshotted_video_path), t=time_stamp)

    return render_template('screenshot_final.html', video_path=screenshotted_video_filename, os=os)


# Change Format of Videos Part
@app.route('/videoformats', methods=['GET','POST'])
def formatvideo():
    return render_template('format.html')

@app.route('/uploadformat', methods=['POST'])
def uploadformat():
    if 'video' not in request.files:
        return "No video file found"
    video = request.files['video']
    if video.filename == "":
        return "No video file selected"
    if video and allowed_file(video.filename):
        # video_filename = secure_filename(video.filename)
        video.save('./static/upload/' + video.filename)
        return render_template('preview_format.html', video_filename_format=video.filename)
    return "Invalid File Type"


@app.route('/finalformat', methods=['GET','POST'])
def format_video():
    video_filename_format = request.form['video_filename_format']
    # selected_format = request.form["video_formats"]
    video_format = request.form["video_format"]

    # original_video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    original_video_path = f"{app.config['UPLOAD_FOLDER']}/{video_filename_format}"
    # edited_folder = app.config['EDITED_FOLDER']


    formatted_video_filename = f"formatted_{video_filename_format.rsplit('.', 1)[0]}"

    # final_edited_folder = Path(edited_folder)
    # edited_filename = formatted_video_filename
    # formatted_video_path = final_edited_folder.joinpath(edited_filename)


    # formatted_video_path = os.path.join(edited_folder, formatted_video_filename)

    video1 = VideoFileClip(original_video_path)

    valid_formats = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg"]
    if video_format in valid_formats:
        formatted_video_filename = f"formatted_{video_filename_format.rsplit('.', 1)[0]}" + video_format
        # formatted_video_path = app.config['EDITED_FOLDER']
        # formatted_video_path = formatted_video_filename + video_format
        formatted_video_path = f"{app.config['EDITED_FOLDER']}/{formatted_video_filename}"
        print('Printing the formatted video path',formatted_video_path)
        
    video1.write_videofile(formatted_video_path, codec="libx264", audio_codec="aac")
    
    # return render_template('format_final.html', video_path=formatted_video_path, os=os)
    edited_folder = app.config['EDITED_FOLDER']
    return send_file(os.path.join(edited_folder, formatted_video_filename), as_attachment=True)

@app.route('/download/<filename>')
def download_1(filename):
    # Use url_for to generate the correct URL for the edited folder
    edited_folder = app.config['EDITED_FOLDER']
    return send_file(os.path.join(edited_folder, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=3050)

