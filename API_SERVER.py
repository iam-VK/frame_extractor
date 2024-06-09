from flask import Flask, request
from flask_cors import CORS
from api_requests import multipart_post
from frame_extractor import extract_keyframes_2, prepare_output_dir
from zipper import zip

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST','GET'])
def service_status():
    return {"Status":'Alive',
            "End-points":{'[POST]':" /keyframe_extract"}
            }

@app.route("/keyframe_extract", methods=['POST'])
def keyframe_extract():
    if request.method == 'POST':   
        file = request.files['file_upload'] 
        if file:
            prepare_output_dir('uploads')
            file_path = f"uploads/{file.filename}"
            file.save(file_path)

        key_frames_return = extract_keyframes_2(file_path)
        key_frames_status = key_frames_return["Status"]

        if key_frames_status == "Success":
            zip('key_frames')

            # return send_file('key_frames.zip', mimetype = 'zip', as_attachment = True)
            post_response = multipart_post(url='http://127.0.0.1:5002/index',
                                           keyframes_dir="key_frames",
                                           file_type="zip",
                                           file_path="key_frames.zip")
            
        print("POST_RESPONSE: ",post_response)
        return key_frames_return

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)