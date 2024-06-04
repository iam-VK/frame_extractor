"""
input: Video.mp4
output: key_frames/img.png
        - number of frames
        - video resolution
        - FPS
        - number of key frames
functionality: extracts key_frames from video using ssim from scikit library
"""

import cv2
from tqdm import tqdm
import os
import glob
from skimage.metrics import structural_similarity as ssim
import numpy as np

def get_video_prop(video_path:str):
    cap = cv2.VideoCapture(video_path)

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"\nTotal number of Frames: {n_frames}")

    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(f'Height {height}, Width {width}')

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'FPS : {fps:0.2f}')

    cap.release()
    
    return n_frames, fps, height, width

def prepare_output_dir(output_path:str):
    isExist = os.path.exists(output_path)
    if isExist:
        old_files = glob.glob(output_path+'/*')
        for f in old_files:
            os.remove(f)
    else:
        os.makedirs(output_path)
    
    return output_path

def calculate_ssim(img1,img2):
    b, g, r = cv2.split(img1)
    prev_b, prev_g, prev_r = cv2.split(img2)
    ssim_b, _ = ssim(prev_b, b, full=True)
    ssim_g, _ = ssim(prev_g, g, full=True)
    ssim_r, _ = ssim(prev_r, r, full=True)
    #print(f"ssim_b:{ssim_b}, ssim_g:{ssim_g}, ssim_r:{ssim_r}")

    similarity_score = (ssim_b + ssim_g + ssim_r) / 3
    #print(f"ssim Score: {similarity_score}")

    return similarity_score

def extract_keyframes(video_path:str, output_dir:str="key_frames",skip_frame_rate:int=3,threshold:int=0.3):  
    cap = cv2.VideoCapture(video_path)
    
    keyframes_dir = prepare_output_dir(output_dir)

    # KeyFrame Extraction
    key_frames = []
    previous_frame = None
    similarity_threshold = threshold #(not sure) range -1(dissimilar) to 1(identical)  
    total_frames, fps, height, width = get_video_prop(video_path)

    for current_frame in tqdm(range(0,total_frames,skip_frame_rate), desc="Extracting Keyframes"):
        ret, img = cap.read()

        if not ret:
            print("Error: Can't access frame")
            break

        if previous_frame is not None:
            # Structural Similarity Index (SSI)
            similarity_score = calculate_ssim(img,previous_frame)
            if similarity_score < similarity_threshold:
                key_frames.append(img)
                # Saving the selected frame to the output directory
                frame_filename = os.path.join(keyframes_dir, f"frame_{current_frame:04d}.png")
                cv2.imwrite(frame_filename, img)
            else:
                frame_filename = os.path.join(keyframes_dir, f"frame_{current_frame:04d}.png")
        else:
            key_frames.append(img)
            # Saving the selected frame to the output directory
            frame_filename = os.path.join(keyframes_dir, f"frame_{current_frame:04d}.png")
            cv2.imwrite(frame_filename, img)

        previous_frame = img

    cap.release()

    print(f'Total key frames based on the threshold chosen : {len(key_frames)}')

def calculate_mse(image1, image2):
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image1.shape[1])
    return err

def extract_keyframes_2(video_path:str, output_dir:str='key_frames',skip_frame_rate:int=3, threshold=8000):
    cap = cv2.VideoCapture(video_path)
    prev_frame = None

    prepare_output_dir(output_dir)

    total_frames, fps, height, width = get_video_prop(video_path)
    n_extracted_frames = 0
    for current_frame in tqdm(range(0, total_frames, skip_frame_rate), desc="Extracting Keyframes",unit='frame', ncols=100):
        ret, frame = cap.read()
        if not ret:
            break

        if prev_frame is not None:
                mse = calculate_mse(prev_frame, frame)
                if mse > threshold:
                    # Save dissimilar frame
                    frame_filename = os.path.join(output_dir, f"frame_{current_frame:04d}.png")
                    cv2.imwrite(frame_filename, frame)
                    n_extracted_frames+=1
        else:
                frame_filename = os.path.join(output_dir, f"frame_{current_frame:04d}.png")
                cv2.imwrite(frame_filename, frame)
                n_extracted_frames+=1 

        prev_frame = frame

    cap.release()
    return {
            "Status" : "Success" if (n_extracted_frames > 0) else "Failed",
            "keyframes extracted" : n_extracted_frames
            }