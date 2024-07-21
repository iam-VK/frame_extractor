from api_requests import *
import os

post_response = multipart_post(url='http://127.0.0.1:5002/index',
                                           keyframes_dir="key_frames",
                                           vid_name=os.path.splitext("market.mp4")[0],
                                           file_type="zip",
                                           file_path="key_frames.zip")
