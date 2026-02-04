# socket-based-quiz-game
socket-based-quiz-game
Bu proje, Python kullanılarak geliştirilen **istemci–sunucu mimarili** bir bilgi yarışması oyunudur.  
Uygulama, gerçek zamanlı socket haberleşmesi, joker mekanizması ve grafik arayüz (GUI) içermektedir.

## Dosyalar

- **Program Sunucusu (`program_sunucusu.py`)**
  - Yarışma akışını yönetir
  - Soruları gönderir
  - Cevapları kontrol eder
  - Joker haklarını takip eder

- **Joker Sunucusu (`joker_server.py`)**
  - Seyirciye Sorma
  - Yarı Yarıya
  - Joker sonuçlarını rastgele ama mantıklı şekilde üretir

- **Yarışmacı Client (`yarismaci_client.py`)**
  - Tkinter ile oluşturulmuş grafik arayüz
  - Soru ve şıkları gösterir
  - Jokerleri görsel olarak uygular
  - Kullanıcıdan cevap alır

## Araçlar

- Python
- Socket Programming (TCP)
- Multithreading
- Tkinter (GUI)
- JSON veri formatı

## Nasıl Çalıştırılır?

### 1️. Joker Sunucusunu Başlat
python joker_server.py
### 2. Program Sunucusunu Başlat
python program_sunucusu.py
### 3. Yarışmacı Arayüzünü Başlat
python yarismaci_client.py
