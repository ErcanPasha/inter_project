### Yeni Sistem Akışı (Human Detection Eklenmiş)

1. **camera\_manager.py**
   ->Kameradan belirli aralıklarla fotoğraf çeker ve son 12 kareyi saklar.
   ->Son iki kareyi change_detector ile karşılaştırır.
   ->Değişim varsa 3 hızlı kare çeker ve tüm fotoğrafları detector'e gönderir.
2. **change\_detector.py**
   ->İki kare arasındaki farkı kontrol eder.
   ->Belirgin değişiklik varsa True, yoksa False döndürür.
3. **detector.py (MediaPipe)**
   ->Gelen karelerde insan sayısını tespit eder (YOLOv4-tiny ile).
   ->Sonuçları txt dosyasına yazar ve klasörler.
   ->uploader'ı çağırarak veriyi ThingsBoard ve Google Drive’a yollar.
4. **uploader.py**
   ->Olay verilerini ThingsBoard’a MQTT ile gönderir.
   ->Fotoğrafları ve txt dosyasını zipleyip Google Drive’a yükler.








