import zipfile
import os

def zip(directory:str):
    zipfolder = zipfile.ZipFile(f'{directory}.zip','w', compression = zipfile.ZIP_STORED)

    for root,dirs, files in os.walk(f'{directory}/'):
            for file in files:
                zipfolder.write(f'{directory}/{file}')
            zipfolder.close()
