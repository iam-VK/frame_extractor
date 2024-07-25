from flask import Flask, request, send_file, url_for
from flask_cors import CORS
from api_requests import multipart_post
from frame_extractor import extract_keyframes_2, prepare_output_dir
from zipper import zip
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST','GET'])
def service_status():
    return {
        "Status":'Alive',
            "End-points": {
                "/keyframe_extract": {
                    "method":"[POST]",
                    "parameters": {
                        "file_upload":"video file for keyframes extraction",
                        "mode":"optional parameter. ['standalone','chained'] chained is the default mode"
                    }
                }
            }
        }

@app.route("/keyframe_extract", methods=['POST'])
def keyframe_extract():
    if request.method == 'POST':   
        file = request.files['file_upload']
        mode = request.form.get('mode',"chained") # other mode:standalone, default mode:chained

        if file:
            prepare_output_dir('uploads')
            file_path = f"uploads/{file.filename}"
            file.save(file_path)

        key_frames_return = extract_keyframes_2(file_path)
        key_frames_status = key_frames_return["Status"]

        if key_frames_status == "Success":
            zip('key_frames')

            if mode == "standalone":
                #return send_file('key_frames.zip', mimetype = 'application/zip', as_attachment = True)
                return {"Frame Extractor service":key_frames_return,
                        "File URL": url_for('download_file', filename='key_frames.zip', _external=True)}
            
            post_response = multipart_post(url='http://127.0.0.1:5002/index',
                                           keyframes_dir="key_frames",
                                           vid_name=os.path.splitext(file.filename)[0],
                                           file_type="zip",
                                           file_path="key_frames.zip")
            
        print("POST_RESPONSE: ",post_response)
        return {"Frame Extractor service":key_frames_return,
                "ViT service":post_response.json()}
    
@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    return send_file(filename, mimetype='application/zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, use_reloader = True)