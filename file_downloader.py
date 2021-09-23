import requests
import os

# import custum libraries
from clint.textui import progress

class FileDownloader():
    def __init__(self, url, custom_path='media', custom_filename=None):
        self.url = url
        self.filename = url.split('/')[-1]
        self.filetype = self.filename.split('.')[-1]
        self.custom_path = custom_path
        self.custom_filename = custom_filename
        self.content_length = 0
        if self.custom_filename:
            self.custom_filetype = custom_filename.split('.')[-1]

    def downlod_file(self):
        try:
            data = requests.get(self.url)
            self.content_length = int(data.headers.get('content-length'))
            print(self.content_length)
            if data.status_code == 200:
                # create directory if not exists
                if not os.path.exists(os.path.join(self.custom_path, self.filetype)):
                    os.makedirs(os.path.join(self.custom_path, self.filetype))

                # custom filename if  given
                if self.custom_filename:
                    # warning if custom filename is not valid.
                    if self.valid_filename():
                        self.filename = self.custom_filename
                        full_path = os.path.join(
                            self.custom_path, self.filetype, self.filename)
                    else:
                        self.filename = f"{self.custom_filename.split('.')[0]}.{self.filetype}"
                        full_path = os.path.join(
                            self.custom_path, self.filetype, self.filename)

                        print(
                            f"[WARNING] Your file type is {self.filename.split('.')[-1]} and you give {self.custom_filename.split('.')[-1]}\n")
                else:
                    full_path = os.path.join(
                        self.custom_path, self.filetype, self.filename)

                with open(f'{full_path}', 'wb') as f:
                    # f.write(data.content)
                    for chunk in progress.bar(data.iter_content(chunk_size=1024), expected_size=(self.content_length/1024) +1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()

                print(
                    f"\n[SUCCESS] {self.filetype} file created successfully at: \n\t[FILE_NAME] {full_path}")
            else:
                print(
                    f"\n[URL NOT_VALID] chack your URL: \n\t[URL = {self.url}]")
                    
        except Exception as e:
            print(f"[ERROR] {e}.")
            return

    def valid_filename(self):
        if self.filetype == self.custom_filetype:
            return True
        else:
            return False
