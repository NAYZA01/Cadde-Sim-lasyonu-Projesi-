import pygame
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
EKRAN_GENISLIK = 800
EKRAN_YUKSEKLIK = 600

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
YOL_GRISI = (50, 50, 50)
SARI = (255, 255, 0)

# Dükkanlar için yeşil tonları (koyu yeşil = düşük yoğunluk, açık = yüksek)
YESIL_TONLAR = [
    (0, 100, 0),    # Çok düşük
    (0, 150, 0),    # Düşük
    (0, 200, 0),    # Orta
    (0, 255, 0),    # Yüksek
    (100, 255, 100) # Çok yüksek
]

# Yoğunluk metinleri (Türkçe)
YOGUNLUK_METINLERI = ["Çok Düşük", "Düşük", "Orta", "Yüksek", "Çok Yüksek"]

# Dükkan veri üretimi
def dukkan_veri_uret():
    urunler = ["Kahve", "Kitap", "Giyim", "Elektronik", "Yemek", "Oyuncak"]
    urun = random.choice(urunler)
    yogunluk_index = random.randint(0, 4)
    yogunluk = YOGUNLUK_METINLERI[yogunluk_index]
    bos_masalar = random.randint(0, 10)
    calisan_sayisi = random.randint(1, 20)
    fiyat_araligi = f"{random.randint(10, 50)} - {random.randint(100, 500)} TL"
    musteri_sayisi = random.randint(0, 50)
    dukkan_ismi = random.choice(["Hızlı Market", "Kitap Evi", "Moda Dükkanı", "Tekno Mağaza", "Lezzet Lokantası", "Oyun Dünyası"]) + f" {random.randint(1, 100)}"
    return {
        "isim": dukkan_ismi,
        "urun": urun,
        "yogunluk": yogunluk,
        "bos_masalar": bos_masalar,
        "calisan_sayisi": calisan_sayisi,
        "fiyat_araligi": fiyat_araligi,
        "musteri_sayisi": musteri_sayisi,
        "yogunluk_index": yogunluk_index
    }

# Dükkan sınıfı
class Dukkan:
    def __init__(self, x, y, genislik, yukseklik):
        self.rect = pygame.Rect(x, y, genislik, yukseklik)
        self.veri = dukkan_veri_uret()
        self.renk = YESIL_TONLAR[self.veri["yogunluk_index"]]

# Araba sınıfı (artık yukarı-aşağı hareket)
class Araba:
    def __init__(self, x, y, hiz):
        self.rect = pygame.Rect(x, y, 20, 40)  # Dikey için boyut değiştir
        self.renk = (random.randint(100, 255), random.randint(0, 100), random.randint(0, 100))
        self.hiz = hiz

    def hareket_et(self):
        self.rect.y += self.hiz
        if self.rect.y > EKRAN_YUKSEKLIK:
            self.rect.y = -40
        elif self.rect.y < -40:
            self.rect.y = EKRAN_YUKSEKLIK

# Ekranı ayarla
ekran = pygame.display.set_mode((EKRAN_GENISLIK, EKRAN_YUKSEKLIK))
pygame.display.set_caption("Cadde Simülasyonu")

# Dükkanları oluştur (sol ve sağ taraf)
dukkanlar = []
dukkan_genislik = 150
dukkan_yukseklik = 100
for i in range(5):  # Sol taraf 5 dükkan
    dukkan = Dukkan(50, 50 + i * (dukkan_yukseklik + 10), dukkan_genislik, dukkan_yukseklik)
    dukkanlar.append(dukkan)

for i in range(5):  # Sağ taraf 5 dükkan
    dukkan = Dukkan(EKRAN_GENISLIK - 200, 50 + i * (dukkan_yukseklik + 10), dukkan_genislik, dukkan_yukseklik)
    dukkanlar.append(dukkan)

# Arabaları oluştur (2-3 tane, yukarı-aşağı hareket)
arabalar = []
araba_sayisi = random.randint(2, 3)
for i in range(araba_sayisi):
    yon = random.choice([1, -1])  # 1: aşağı, -1: yukarı
    hiz = random.randint(2, 5) * yon
    x_pos = EKRAN_GENISLIK // 2 + (i * 30) - 30  # Yol ortasında
    y_pos = random.randint(0, EKRAN_YUKSEKLIK) if yon == 1 else EKRAN_YUKSEKLIK
    araba = Araba(x_pos, y_pos, hiz)
    arabalar.append(araba)

# Popup bilgi
secili_dukkan = None
yazi_tipi = pygame.font.Font(None, 24)
isim_yazi_tipi = pygame.font.Font(None, 20)

# Ana döngü
calisiyor = True
saat = pygame.time.Clock()

while calisiyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            calisiyor = False
        elif olay.type == pygame.MOUSEBUTTONDOWN:
            fare_pos = pygame.mouse.get_pos()
            secili_dukkan = None
            for dukkan in dukkanlar:
                if dukkan.rect.collidepoint(fare_pos):
                    secili_dukkan = dukkan
                    break

    # Arka planı çiz
    ekran.fill(SIYAH)

    # Yolu çiz (dikey yol)
    yol_rect = pygame.Rect(EKRAN_GENISLIK // 2 - 100, 0, 200, EKRAN_YUKSEKLIK)
    pygame.draw.rect(ekran, YOL_GRISI, yol_rect)

    # Sarı çizgileri çiz (dikey için yatay çizgiler)
    for x in range(EKRAN_GENISLIK // 2 - 50, EKRAN_GENISLIK // 2 + 50, 100):
        for y in range(0, EKRAN_YUKSEKLIK, 50):
            pygame.draw.line(ekran, SARI, (x, y), (x, y + 20), 5)

    # Dükkanları çiz ve isimlerini yaz
    for dukkan in dukkanlar:
        pygame.draw.rect(ekran, dukkan.renk, dukkan.rect)
        # Dükkan ismini yaz
        isim_yazi = isim_yazi_tipi.render(dukkan.veri["isim"], True, BEYAZ)
        ekran.blit(isim_yazi, (dukkan.rect.x + 10, dukkan.rect.y + 10))

    # Arabaları çiz ve hareket ettir
    for araba in arabalar:
        araba.hareket_et()
        pygame.draw.rect(ekran, araba.renk, araba.rect)

    # Seçiliyse popup çiz
    if secili_dukkan:
        popup_metin = (
            f"İsim: {secili_dukkan.veri['isim']}\n"
            f"Satıyor: {secili_dukkan.veri['urun']}\n"
            f"Müşteri Yoğunluğu: {secili_dukkan.veri['yogunluk']}\n"
            f"Boş Masalar: {secili_dukkan.veri['bos_masalar']}\n"
            f"Çalışan Sayısı: {secili_dukkan.veri['calisan_sayisi']}\n"
            f"Fiyat Aralığı: {secili_dukkan.veri['fiyat_araligi']}\n"
            f"Mevcut Müşteri Sayısı: {secili_dukkan.veri['musteri_sayisi']}"
        )
        satirlar = popup_metin.split('\n')
        popup_genislik = 300
        popup_yukseklik = len(satirlar) * 25 + 20
        popup_x = EKRAN_GENISLIK // 2 - popup_genislik // 2
        popup_y = EKRAN_YUKSEKLIK // 2 - popup_yukseklik // 2
        pygame.draw.rect(ekran, BEYAZ, (popup_x, popup_y, popup_genislik, popup_yukseklik))
        for i, satir in enumerate(satirlar):
            yazi_yuzey = yazi_tipi.render(satir, True, SIYAH)
            ekran.blit(yazi_yuzey, (popup_x + 10, popup_y + 10 + i * 25))

    pygame.display.flip()
    saat.tick(60)

pygame.quit()