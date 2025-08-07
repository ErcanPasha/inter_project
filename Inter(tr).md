📌 Bu README Hakkında

 	Bu dosya, sadece yaptığım projeyi tanıtmak için yazılmadı. Aynı zamanda bu projeyle uğraşırken aklıma takılan, üzerine düşündüğüm ve keşke daha önce bilseydim dediğim şeyleri de bir araya getirdiğim bir not defteri gibi düşünebilirsiniz. Teknik bir rapordan çok, deneyim odaklı bir özet olsun istedim. Elbette bu süreçte notlarımda eksiklik, hata veya gözden kaçırmış olduğum noktalar olabilir. Bunlar için şimdiden özürlerimi iletmek isterim 😅.

 

 	Staja başlamadan önce Raspberry Pi benim için sadece adını duyduğum "minik bir bilgisayardı." Ne işe yaradığını, ne kadar geniş bir kullanım alanı olduğunu, sanıldığı kadar kısıtlı olmadığını ve bu kadar güçlü bir yapıya sahip olduğunu bu süreçte öğrenmeye başladım. Özellikle proje fikrini geliştirme aşamasında bu bakış açısı değişikliği bende çok şey etkiledi.



 	Ben genelde fikirlerimi ve notlarımı sistematik bir şekilde tutmayı severim. Ama bu düzen, başkalarının ilk bakışta anlamasını biraz zorlaştırabiliyor. Dosya yollarım, notlarım veya klasör yapılarım karışık görünse de, bana odaklanma ve hatırlama konusunda ciddi katkı sağlıyor. Staj süresince ne kadar çok şey denediğimi ve öğrendiğimi fark ettikçe bu da bir yöntemin parçasıymış dedim.



🚏 PTE\_SSDMS Proje Süreci ve Kendi Öğrendiklerim

❗ Fikir Bulmak Zaman Alıyor

 	Stajın başında proje fikrini oluşturmak düşündüğümden daha zor oldu. Raspberry Pi ve Sixfab Modem Kit gibi donanımların potansiyelini yeni yeni kavrarken, gerçekten işe yarayacak bir fikir bulmak kolay olmadı. Sırf “bir şey yapmış olmak için” bir ürünle uğraşmak istemiyordum. Bu yüzden proje konusunda karar verene kadar çokça zaman ve enerji harcadım ama iyi ki öyle olmuş.


📚 Bilmediğim Her Şeyi Not Ettim

 	Proje süresince aklıma takılan her terimi, denediğim her şeyi bir yerlere not ettim. Gerekli gereksiz demeden. Geriye dönüp baktığımda o notların neredeyse hepsi bir noktada işe yaradı. Bu sürede sadece proje değil; Git kullanımı, rclone ile bulut entegrasyonu, ThingsBoard gibi platformlar, MediaPipe/OpenCV gibi araçlar hakkında da çok şey öğrendim. Hepsi başta karmaşık gelse de zamanla sistemli bir bütün haline geldi.


💡 Proje Fikri, Öğrenme Süreci ve Kendi Notlarım

&nbsp;	Proje fikrinde hem fikir olduğumuzda, neredeyse her şey benim için yeniydi. Raspberry Pi daha önce sadece adını duyduğum bir cihazdı. Git’i sadece birkaç defa push için kullanmıştım. IoT, ThingsBoard, AT command’ler, image processing konuları… hepsi ya hiç bilmediğim ya da sadece isim olarak tanıdığım alanlardı. İşte bu yüzden, staj boyunca gerekli gereksiz demeden birçok şeyi not aldım. Aklıma takılan terimler, uygulamalar, hata mesajları, donanım-yazılım arası etkileşimler, hatta bazen sadece "bu neydi ya?" dediğim detaylar bile bugün dönüp baktığımda çok işime yaradı.


🎯 Projenin Genel Yapısı

&nbsp;	PTE\_SSDMS (Public Transportation Efficiency with Smart Stop Density Monitoring System) isminden de anlaşılabileceği gibi, otobüs duraklarında olan hareketliliği tespit edip, yolcu varlığına göre hem kullanıcıyı hem sistemi bilgilendirmeyi amaçlayan bir sistem. Basit bir fikir gibi görünse de, özellikle büyük şehirlerdeki ulaşım optimizasyonu için ciddi bir fayda potansiyeli taşıyor.

Sistemin temel yapısı:

* Raspberry Pi ve kamera ile görüntü yakalama
* Görüntüler arasında fark tespiti (change detection)
* Fark varsa, insan var mı yok mu? sorusuna cevap arama
* Varsa: ThingsBoard’a bildirim, Google Drive’a 12 görüntülük zip arşivi gönderimi
* Tüm sistem Python ile yazıldı ve rclone, paho-mqtt, OpenCV gibi araçlarla desteklendi 


📡 AT Komutlarıyla Tanışmam

&nbsp;	Bu süreçte belki de en az bilinen ama en çok işe yarayan şeylerden biri AT komutları (AT commands) oldu. İlk başta “neden bu kadar karışık?” diye düşünmüştüm ama temel yapısını anlayınca aslında çok mantıklı bir sistem olduğu ortaya çıktı. Bu kısmın kurulumu vs de gayet basit halledilebilir.
	
&nbsp;	Eğer bu projeye başlamadan önce AT komutlarının mantığını okumuş olsaydım, birçok şeyi daha hızlı çözebilirdim. O yüzden aşağıya hem bir tablo, hem de ileride kendime referans olması için bazı temel komutları bırakıyorum:

📎 (Not: Yakında buraya AT komutlarıyla ilgili PDF kaynağımın linkini bırakacağım. Başlık sırası ile pdf uyuşmuo olabilir. Gpt bu konuda beni kandırdı xd)

| No | Başlık                 | Örnek Kullanım                  |

| -- | ---------------------- | ------------------------------- |

| 1  | Basic commands         | `AT`, `ATI`, `ATE0`             |

| 2  | Call Control           | `ATA`, `ATH`, `AT+CLCC`         |

| 3  | Network Service        | `AT+COPS`, `AT+CREG`            |

| 4  | SMS                    | `AT+CMGF`, `AT+CMGS`, `AT+CMGR` |

| 5  | Packet Domain          | `AT+CGDCONT`, `AT+CGACT`        |

| 6  | Phonebook              | `AT+CPBS`, `AT+CPBR`            |

| 7  | Supplementary Services | Çağrı yönlendirme vb.           |

| 8  | Audio                  | Mikrofon/ses ayarları           |

| 9  | Clock                  | Saat ayarı                      |

| 10 | SIM Toolkit            | Gelişmiş SIM servisleri         |

| 11 | GPIO                   | Dijital pin kontrolü            |

| 12 | GNSS                   | GPS konumu alma                 |

| 13 | File system            | Dahili hafıza ile dosya yaz/oku |

| 14 | HTTP/FTP/SSL           | Web’e veri gönderme / alma      |



🧰 Git Komutları – Ezber Değil, Gerçek Anlayış

&nbsp;	Projenin ilerleyen aşamalarında Git'e daha fazla ihtiyaç duydukça, bazı temel komutlar ve kavramlar benim için oldukça kritik hale geldi. Daha önce sadece birkaç git push yapmıştım ama bu süreçte Git’in aslında ne kadar güçlü ve esnek bir sistem olduğunu deneyimledim. Aşağıda hem öğrendiğim komutları, hem de kendi yorumlarımı başlıklar halinde toparladım. 

Unutmadan: 💻 Tüm adımlar Windows üzerinde cmd kullanılarak yapıldı.
1. Başlarken
   	Git'e başlamadan önce git --version komutuyla sistemde kurulu olup olmadığını ve güncel olup olmadığını kontrol etmek iyi bir adımdı. Sonrasında, bir dosya ile Git arasında bağlantı kurmanın iki yolu var:
   	->**git clone <URL>:** Uzaktaki bir repoyu hızlıca yerel bilgisayara kopyalar
   	->**git init:** İçinde bulunduğun klasörü bir Git reposuna çevirir. .git adlı gizli bir klasör oluşturur ve bu klasörde Git'in kontrol mekanizması başlar.(Bu projede git init yolunu kullandım)
   
2. Uzak Repo Tanımlama
   git init sonrası Git'i bir uzak repoyla eşleştirmek gerekir:
   	**->git remote add origin <URL>:** Uzak repo bağlantısını kurar.
   	**->git push -u origin main:** Ana branch’i (eski adıyla "master") oluşturur ve ilk gönderimi yapar.
   	**->git pull origin main:** Uzakta yapılan değişiklikleri yerel makineye çeker. Ancak eğer sadece tek kişilik, lokal odaklı bir repo kullanıyorsanız, bu komut her zaman gerekli olmayabilir
   🥨Ekstra olarak:
   	**->git remote remove origin:** Bağlantıyı koparır ama .git klasörü içeride kalır
   	->**rmdir /s /q .git:** .git klasörünü komple siler ve geçmiş bağlantıları tamamen kaldırır. Geri dönüşü yok, dikkatli kullanmak gerek.
   
3. Dosya Takibi – Stage ve Commit Süreci
   	Burada işler biraz daha ilginçleşiyor. Dosya sisteminde yaptığın değişiklikler Git'e otomatik olarak yansımaz. Bu yüzden “ne göndermek istiyorsun?” sorusuna cevap olarak önce dosyaları Stage adı verilen alana eklemen gerekiyor.
   	**->git add .:** Tüm dosyaları stage alanına ekler
   	**->git add dosya\_adi :** Sadece belirli bir dosyayı eklersin
   	**->git reset:** Stage'i temizler
   	**->git commit -m "açıklama":** Stage'deki dosyaları Git geçmişine bir açıklamayla kaydeder
   	**->git commit --amend -m "yeni açıklama":** Son commit mesajını günceller. (Bu komut yalnızca henüz push yapılmamışsa işe yarar)
   🍜Ayrıca:
   	**->git status:** Stage’e ne eklenmiş, ne eksik, ne silinmiş… her şeyi gösteren kontrol komutu
   	**->git rm --cached dosya\_adi:** Dosya Git geçmişinde kalır ama artık aktif olarak takip edilmez
   	**->git rm dosya\_adi:** Dosyayı tamamen siler
   
4. Branch (Dal) Mantığı
   	Git'in en sevdiğim yanlarından biri de branch sistemi. Çünkü farklı fikirleri ayrı ayrı test edebilmek, çalışmaları karıştırmadan ilerletmek mümkün oluyor.
   	**->git branch:**boş bırakıldığında güncel lokalindeki branchleri ve hangi branch üzerinde olduğunu gösteriyor. Hangi branch üzerinde olduğn önemli çünkü mlsf push yaparken push işlemini sadece üstünde bulunduğun branch'e yapabilrisin
   	**->git checkout -b deneme\_branchi:**branch oluşturarak başlayalım. deneme\_branchi isminde bir branch (dal) oluşturur
   	**->git checkout branch\_adi:** branch\_adi isimli branch'e geçmeni sağlar
   	**->git branch -M yeni\_ana\_branch:** default olarak main branch ana branch'indir fakat bunu değiştirebilrsin
   	**->git branch -d branch\_adi:** lokalde açtığın gereksiz veya artık kurutlmak istediğin ilgili branch'i siler
   	**->git push origin --delete branch\_adi:** Uzak (origin) branch’i siler
   	**->git merge branch\_x:** Aktif olduğun branch’e, branch\_x’in içeriğini birleştirir
   	**->git branch -m eski\_isim yeni\_isim:** Branch ismini değiştirir
   Branch’ler sayesinde hem karmaşıklık azalıyor, hem de büyük değişiklikleri test etmeden önce ayrı bir alanda denemek mümkün oluyor. 

&nbsp;	Bu komutları öğrenmek benim için sadece bir "araç" öğrenmek değil, aynı zamanda bir "çalışma alışkanlığı" kazanmak oldu. Sürekli hata yapıp çözümlerini ararken fark ettim ki; Git, sadece bir sürüm kontrol sistemi değil, aynı zamanda bir düşünme biçimi kazandırıyor. Daha çok komutu mevcut fakat bunların başlangıç için iyi ve yeterli olduğunu düşünüyorum.