import requests
import os
import time

# import custum libraries
from tqdm import tqdm


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
            self.content_length = int(data.headers.get('content-length', 0))
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

                total_size_in_bytes= self.content_length
                block_size = 1024 #1 Kibibyte
                progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
                with open(f'{full_path}', 'wb') as f:
                    for d in data.iter_content(block_size):
                        progress_bar.update(len(d))
                        f.write(d)
                progress_bar.close()
                if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                    print("[WARNING] something went wrong with progress bar size.")

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
