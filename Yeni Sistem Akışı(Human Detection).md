### Yeni Sistem Akışı (Human Detection Eklenmiş)

1. **camera\_manager.py
   ->**Belirli zaman aralıklarında fotoğraf çekmeye devam eder ve 1 dakikalık (son 12 fotoğraf) buffer tutar.
   ->change\_detector.py tarafından tetiklenirse, ek olarak n+1 fotoğraf veya kısa seri (2–3 kare) çeker.
   ->Bu kare(ler) detector.py'ye yönlendirilir.
2. **change\_detector.py
   ->**Son çekilen kare ile bir önceki kareyi karşılaştırır.
   ->Anlamlı değişim tespit edilirse → detector.py çağrılır.
3. **detector.py (MediaPipe)
   ->**Kamera modülünden gelen kare(ler)i alır.
   ->MediaPipe kullanarak insan tespiti yapar ve toplam kişi sayısını döndürür.
   ->Sonucu (kişi sayısı + kareler) event\_handler mantığına aktarır.
4. **event\_handler.py (önceki sürümlerde olduğu gibi)**
   ->İnsan tespit olayını işler
   ->uploader.py'yi çağırarak
6. **uploader.py**
   ->ThingsBoard ve Google Drive API / rclone entegrasyonu ile veri ve görselleri sisteme gönderir.








