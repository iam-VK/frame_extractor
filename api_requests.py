import requests

def multipart_post(url:str,keyframes_dir:str,file_type:str,file_path:str):
    data = {'keyframes_dir': keyframes_dir,
            'file_type':file_type}

    files = {'file_upload': open(file_path, 'rb')}

    response = requests.post(url, data=data, files=files)

    return response
