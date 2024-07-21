import requests

def multipart_post(url:str,vid_name:str,keyframes_dir:str,file_type:str,file_path:str):
    data = {'vid_name':vid_name,
            'dir': keyframes_dir,
            'file_type':file_type}

    files = {'file_upload': open(file_path, 'rb')}

    response = requests.post(url, data=data, files=files)

    return response
