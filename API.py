from flask import Flask, request, send_file
from flask_cors import CORS
from frame_extractor import extract_keyframes_2
from zipper import zip

app = Flask(__name__)
CORS(app)

@app.route("/keyframe_extract")
def keyframe_extract():
    file_path = request.args['file_path']

    key_frames_return = extract_keyframes_2(file_path)
    
    key_frames_status = key_frames_return["Status"]
    if key_frames_status == "Success":
        zip('key_frames')

        return send_file('key_frames.zip',
                mimetype = 'zip',
                as_attachment = True)
    return key_frames_return

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)