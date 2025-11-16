import random
from figur import sekiller
from renkler import Renkler
import os
import json

sag_ok = "\U000027A1\U0000FE0F"  # ➡️ (Sağ Ok)
bilgi="\U00002139\U0000FE0F"    # ℹ️ (Bilgi İşareti)
kupa="\U0001F3C6"
soru_isareti="\U00002753"
girdi_isareti = "\U0001F449"

kategoriler = {
    "hayvanlar": ["kedi", "köpek", "kuş", "fil"],
    "meyveler": ["elma", "muz", "çilek", "portakal"],
    "renkler": ["mavi", "yeşil", "kırmızı", "sarı"]
}

global secilen_kategori
global secilen_kelime
global puan
global bonus
global can
global gizli_kelime
global girilen_karakterler
dosya_adi = "scores.json"

def figur_goster(can):
    print(sekiller[can])

def kategori_sec():
    global secilen_kategori
    kategori_anahtarlari = list(kategoriler.keys())
    secilen_kategori = random.choice(kategori_anahtarlari)
    print(f"{Renkler.SARI}Sistem tarafından bir kategori seçildi. {Renkler.RESET}")

def kelime_sec():
    global secilen_kelime , gizli_kelime
    secilen_kelime = random.choice(kategoriler[secilen_kategori])
    gizli_kelime = len(secilen_kelime)* "_ "
    print(f"{Renkler.SARI}Sistem tarafından bir kelime seçildi. {Renkler.RESET}")

def harfi_kontrol_et(karakter):
    global secilen_kelime
    global gizli_kelime
    global puan
    global can

    if karakter not in secilen_kelime:
        puan -= 5
        can -= 1
        print(f"Yanlış tahmin! '{karakter}' kelimede yok.")
    else:
        for i in range(len(secilen_kelime)):
            if secilen_kelime[i] == karakter:
                gizli_kelime = gizli_kelime[:i*2] + karakter + gizli_kelime[i*2+1:]
        puan += 10
        print(f"Tebrikler! '{karakter}' kelimede var.\n")

def kullanicidan_harf_al():
    while True:
        harf = input("Bir harf tahmin edin: ").lower()
        if len(harf) == 1 and harf.isalpha() and harf not in girilen_karakterler:
            girilen_karakterler.append(harf)
            return harf
        else:
            print("Lütfen geçerli bir harf girin.")

def tahminleri_goster(girilen_karakterler):
    if(len(girilen_karakterler) > 0):
        print(f"Girilen Harfler: {girilen_karakterler}")

def ipucu_goster(b):
    global bonus, secilen_kategori
    if bonus == 0:
        print("İpucu kullanmak için yeterli bonus puanınız yok.")
        return
    
    print("Seçilen kategoriye ait bir ipucu veriliyor...")
    print(f"İpucu: Seçili kategori: '{secilen_kategori}'")
    bonus -=1

def islem_turu_sec():
    islem_turleri = ["toplama", "çıkarma", "çarpma", "bölme","iptal"]
    while True:
        islem_turu = input(f"{girdi_isareti}İşlem türü (toplama/çıkarma/çarpma/bölme) ya da 'iptal':").lower()
        if islem_turu in islem_turleri:
            return islem_turu
        else:
            print("Geçersiz işlem türü. Lütfen tekrar işlem türü seçin.")

def sayi_al(hangi_sayi,islem_turu):
    while True:
        s = input(f"{girdi_isareti}{hangi_sayi}. sayı (iptal için 'iptal): ").lower()
        if s == "iptal":
            return "iptal"
        if islem_turu == "bölme" and hangi_sayi == 2 and s == "0":
            print("Bölen sıfır olamaz. Lütfen tekrar deneyin.")
            continue
        try:
            return int(s)
        except ValueError:
            print("Geçersiz sayı. Lütfen tekrar deneyin.")

def iptal_kontrol(secim):
    if str(secim).lower() == "iptal":
        print("İşlem iptal edildi.")
        return True
    return False

def islem_coz(islem_turu, sayi1, sayi2):
    global can
    islem_operatoru = ""
    if islem_turu == "toplama":
        islem_operatoru = "+"
        dogru_sonuc = sayi1 + sayi2
    elif islem_turu == "çıkarma":
        islem_operatoru = "-"
        dogru_sonuc = sayi1 - sayi2
    elif islem_turu == "çarpma":
        islem_operatoru = "*"
        dogru_sonuc = sayi1 * sayi2
    elif islem_turu == "bölme":
        islem_operatoru = "/"
        dogru_sonuc = sayi1 / sayi2
    global bonus
    print(f"{soru_isareti}Soru: {sayi1} {islem_operatoru} {sayi2} = ?")
    while True:
        cevap = input(f"{girdi_isareti}Cevabınız: ").lower()
        try:
            if float(cevap) == dogru_sonuc:
                print("Doğru!")
                random_karakter_ac()
                bonus += 1
                print(f"Bonus puan kazandınız! Toplam bonus: {bonus}")
                break
            else:
                print(f"Yanlış! Doğru cevap: {dogru_sonuc}")
                can -= 1
                break
        except ValueError:
            print("Geçersiz cevap. Lütfen tekrar deneyin.")

def random_karakter_ac():
    global gizli_kelime
    global secilen_kelime
    global girilen_karakterler
    # Boş olan indisleri bul (sadece _ olan yerler)
    bos_indisler = []
    for i in range(len(secilen_kelime)):
        if gizli_kelime[i*2] == "_":
            bos_indisler.append(i)
    
    if not bos_indisler:  # Eğer tüm harfler açıksa
        return
        
    # Rastgele bir boş indis seç
    rastgele_indeks = random.choice(bos_indisler)
    # Seçilen indisteki karakteri al
    acilacak_karakter = secilen_kelime[rastgele_indeks]
    
    # Bu karakterin geçtiği tüm yerleri aç
    for i in range(len(secilen_kelime)):
        if secilen_kelime[i] == acilacak_karakter:
            gizli_kelime = gizli_kelime[:i*2] + acilacak_karakter + gizli_kelime[i*2+1:]
    
    print(f"{Renkler.SARI}Bonus! '{acilacak_karakter}' harfi açıldı{Renkler.RESET}")
    girilen_karakterler.append(acilacak_karakter)

def secenek_al():
    dogru_secimler = ["H", "İ", "I", "Ç", "Q","h", "i", "ı", "ç", "q"]
    while True:
        print(f"\n{sag_ok} Seçenekler [H]arf Tahmini | [İ]şlem Çöz | [I]pucu | [Ç]ıkış (Q)")
        secim = input(f"{girdi_isareti}Seçiminiz: ")
        if secim in dogru_secimler:
            if secim == "i" :
                return "İ"
            return secim.upper()
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

def puan_kaydet_json(puan):
    isim = input("Skor tablosuna kaydetmek için isminizi girin: ")
    yeni_kayit = {"isim": isim, "puan": puan}
    skorlar = []
    
    if os.path.exists(dosya_adi):
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            dosya_icerigi = f.read()
            skorlar = json.loads(dosya_icerigi)

    skorlar.append(yeni_kayit)
    skorlar.sort(key=lambda x: x['puan'], reverse=True)
    try:
        # 'w' modu her zaman yeni/güncel içeriği yazar (dosya yoksa oluşturur).
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(skorlar, f, indent=4, ensure_ascii=False)
        print(f"🎉 Başarılı: '{isim}' için {puan} skoru '{dosya_adi}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Hata: Veri yazılırken bir sorun oluştu: {e}")

def puan_tablosunu_goster():
    with open(dosya_adi, 'r', encoding='utf-8') as f:
        skorlar = json.load(f)

    if not skorlar:
        print(f"Skor tablosu boş.")
        return
    
    skorlar.sort(key=lambda x: x['puan'], reverse=True)

    top_5 = skorlar[:5]
    print("\n" + "="*30)
    print("🥇 EN İYİ 5 SKOR TABLOSU 🥈")
    print("="*30)
    print(f"{'Sıra':<5}{'İsim':<15}{'Puan'}")
    print("-" * 30)
    
    for i, kayit in enumerate(top_5, 1):
        print(f"{i:<5}{kayit['isim']:<15}{kayit['puan']}")
    
    print("="*30 + "\n")

def oyun_baslat():
    global girilen_karakterler
    global puan
    global bonus
    global can
    girilen_karakterler = []
    puan = 0
    bonus = 0
    can = 6
    print(f"{Renkler.YESIL}Oyun başladı! {Renkler.RESET}")
    kategori_sec()
    kelime_sec()

    while can > 0:
        print("\n--- Yeni Tur ---\n")
        figur_goster(can)
        print(f"Kelime: {gizli_kelime}")
        tahminleri_goster(girilen_karakterler)
        print(f"{bilgi} Puan: {puan}, Bonus: {bonus}, Hak: {can}")
        secim=secenek_al()

        if secim == "Ç" or secim == "Q":
            print("Oyundan çıkılıyor.")
            break
        elif secim == "H":
            harf = kullanicidan_harf_al()
            harfi_kontrol_et(harf)
        elif secim == "I":
            ipucu_goster(bonus)
        elif secim == "İ":
            islem_turu = islem_turu_sec()
            if iptal_kontrol(islem_turu):
                continue
            sayi1 = sayi_al(1,islem_turu)
            if iptal_kontrol(sayi1):
                continue
            sayi2 = sayi_al(2,islem_turu)
            if iptal_kontrol(sayi2):
                continue
            islem_coz(islem_turu, sayi1, sayi2)

        if "_" not in gizli_kelime:
            print(f"\n{kupa}Tebrikler! Kelimeyi buldunuz: {secilen_kelime}")
            puan += 50
            print(f"{kupa}Toplam Puanınız: {puan}")
            break
        if can == 0:
            figur_goster(can)
            puan-= 20
            print(f"Oyunu kaybettiniz. Doğru kelime {secilen_kelime}")
            print (f"Toplam puanınız:{puan}")
            break
    
    if secim != "Ç" and secim != "Q":
        puan_kaydet_json(puan)
    puan_tablosunu_goster()

oyun_baslat()