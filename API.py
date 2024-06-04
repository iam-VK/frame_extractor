from flask import Flask, request
from flask_cors import CORS
from frame_extractor import extract_keyframes_2

app = Flask(__name__)
CORS(app)

@app.route("/keyframe_extract", methods=['GET'])
def keyframe_extract():
    if request.method == 'GET':
        file_path = request.args['file_path']
        print("file_path -> ",file_path)
        return extract_keyframes_2(file_path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)