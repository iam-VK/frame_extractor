from flask import Flask, request, send_file
from flask_cors import CORS
from frame_extractor import extract_keyframes_2, prepare_output_dir
from zipper import zip
import os 

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST','GET'])
def service_status():
    return {"Status":'Alive',
            "End-points":{'[POST]':" /keyframe_extract",}
            }

@app.route("/keyframe_extract", methods=['POST'])
def keyframe_extract():
    prepare_output_dir('uploads')
    if request.method == 'POST':   
        file = request.files['file'] 
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        key_frames_return = extract_keyframes_2(file_path)
        key_frames_status = key_frames_return["Status"]

        if key_frames_status == "Success":
            zip('key_frames')
            
            return send_file('key_frames.zip', mimetype = 'zip', as_attachment = True)
        
        return key_frames_return

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':   
#             file = request.files['file'] 
#             file.save(os.path.join('uploads', file.filename))
#     return {'File upload success!':202}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)