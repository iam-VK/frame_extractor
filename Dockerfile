FROM python

WORKDIR /app 

COPY API_SERVER.py      \ 
    api_requests.py     \
    frame_extractor.py  \
    zipper.py           \
    requirements.txt    \
    clean_cache.sh      \
    /app/

RUN apt update
RUN apt-get install libgl1-mesa-glx -y

RUN pip install -r /app/requirements.txt

EXPOSE 5001

CMD python API_SERVER.py