from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GoogleDriveClient:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.CommandLineAuth()
        self.drive = GoogleDrive(gauth)
    
    def download_all_files(self, folder_id, output_path):
        list_files = self.drive.ListFile({
            'q': "'{}' in parents and trashed=false".format(folder_id)
        }).GetList()

        for files in list_files:
            for file in self.get_files(files):
                file.GetContentFile(f"{output_path}/{file['title']}")

    def get_files(self, file):
        if (file['mimeType'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
            return [file]
        else:
            list_files = self.drive.ListFile({
                'q': "'{}' in parents and trashed=false".format(file['id'])
            }).GetList()
            
            return [file for files in list_files for file in self.get_files(files)]

if (__name__ == "__main__"):
    client = GoogleDriveClient()

    drive_id = 'GOOGLE_DRIVE_ID_TO_DOWNLOAD'
    output_path = 'YOUR_TARGET_OUTPUT_FOLDER'
    
    client.download_all_files(drive_id, output_path)