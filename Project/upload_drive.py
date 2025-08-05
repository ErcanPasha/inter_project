from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Sadece dosya yükleme için gerekli izin
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def main():
    creds = None
    # Daha önce yetkilendirilmişse, token.json dosyasını kullan
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Yetkilendirme bilgilerini kaydet
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Drive servisini oluştur
    service = build('drive', 'v3', credentials=creds)

    # Yüklenecek dosya adı
    file_metadata = {'name': 'deneme_foto.jpg'}
    media = MediaFileUpload('Images/img_10.jpg', mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('Dosya Yüklendi. ID:', file.get('id'))

if __name__ == '__main__':
    main()
