import random #random olarak seçmek için kütüphane ekledik

def kategori_getir(): #kategori seçimi için kontrol sağladık
    while True:
        kategori_secimi = input().lower() #büyük-küçük harf duyarlılığını sağladık
        if kategori_secimi in kategoriler:
            return kategori_secimi 
        else:
            print("Yanlış giriş yapıldı.Lütfen kategori seçiniz!!")


def kelime_getir(secilen_kategori): #girilen kategoriye göre listeden rastgele eleman döndürdük
    if secilen_kategori == "hayvan":
        secilen = random.choice(hayvan_list)
    elif secilen_kategori == "meyve":
        secilen = random.choice(meyve_list)
    elif secilen_kategori == "teknoloji":
        secilen = random.choice(teknoloji_list)
    return secilen

kategoriler = ["hayvan", "meyve", "teknoloji"]
hayvan_list = ["civciv", "öküz", "kedi", "köpek", "koyun", "kurbağa", "inek", "ceylan", "aslan"]
meyve_list = ["çilek", "muz", "elma", "erik", "armut", "şeftali", "ananas"]
teknoloji_list = ["telefon", "tablet", "bilgisayar", "kulaklık"]

print("Kategorinizi seçiniz: [Hayvan], [Meyve], [Teknoloji]")
puan=0 
bonus=0
secilen_kategori = kategori_getir()
kelime = kelime_getir(secilen_kategori)
tahmin_kelime= len(kelime)* "_ "
hak_sayisi=6

girilen_harfler= [] #karakterin kontrolünü sağlamak için tanımladık

def karakter_al(): #her turda karakter alımını sağlar
    while True:
        kullanici_karakteri= input("Karakter giriniz:")
        if kullanici_karakteri.isalpha() and len(kullanici_karakteri)==1 and kullanici_karakteri not in girilen_harfler:
            #karakter metin mi tek bir karakter mi ve daha önce girilmiş mi kontorlünü yapar
            girilen_harfler.append(kullanici_karakteri) #karakter uygunsa listeye ekler
            return kullanici_karakteri
        else:
            print("Lütfen tek bir karakter girişi yapınız")
        
def girilen_karakteri_kontrol_et(girilen_karakter):
    global hak_sayisi, tahmin_kelime , puan # global değişkenleri kullanacağımızı belirtiyoruz
    if girilen_karakter not in kelime:
        puan-= 5
        hak_sayisi -= 1  # bir azaltma işlemi
        print("Yanlış tahmin! Kalan hak:", hak_sayisi)
    else:
        # Kelimenin içinde karakterin bulunduğu tüm indisleri bul
        for i in range(len(kelime)):
            if kelime[i] == girilen_karakter:
                puan+=10
                # Tahmin kelimesini güncelle
                tahmin_kelime = tahmin_kelime[:i*2] + girilen_karakter + tahmin_kelime[i*2+1:]
        print("Doğru tahmin! Kelime:", tahmin_kelime)

def random_karakter_ac():
    global tahmin_kelime
    # Boş olan indisleri bul (sadece _ olan yerler)
    bos_indisler = []
    for i in range(len(kelime)):
        if tahmin_kelime[i*2] == "_":
            bos_indisler.append(i)
    
    if not bos_indisler:  # Eğer tüm harfler açıksa
        return
        
    # Rastgele bir boş indis seç
    rastgele_indeks = random.choice(bos_indisler)
    # Seçilen indisteki karakteri al
    acilacak_karakter = kelime[rastgele_indeks]
    
    # Bu karakterin geçtiği tüm yerleri aç
    for i in range(len(kelime)):
        if kelime[i] == acilacak_karakter:
            tahmin_kelime = tahmin_kelime[:i*2] + acilacak_karakter + tahmin_kelime[i*2+1:]
    
    print(f"Bonus! '{acilacak_karakter}' harfi açıldı")


def oyun():
    global hak_sayisi, puan, bonus
    while True:
        print( "Tahmin edilecek kelime:", tahmin_kelime)
        print(f"Kalan hak: {hak_sayisi}")
        print(f"Puan: {puan}")
        print("Seçenekler: [H]arf Tahmini - [I]şlem Çöz - [İ]pucu - [Ç]ıkış")
        secim = input("Seçiminiz: ").upper()
        
        if secim == "Ç":
            break
        elif secim == "H":
            karakter = karakter_al()
            girilen_karakteri_kontrol_et(karakter)
        elif secim == "I":
            sonuc = islem_yap()
            if sonuc is not None:  # sıfıra bölme hatası olmadığında
                kullanici_sonuc = float(input("İşlem sonucunu giriniz: "))
                if abs(kullanici_sonuc - sonuc) < 0.01:  # float karşılaştırması için küçük bir tolerans
                    bonus += 1
                    puan += 15
                    random_karakter_ac()
                    print("Doğru! Bonus kazandınız!")
                else:
                    hak_sayisi -= 1
                    puan -= 10
                    print(f"Yanlış! Doğru cevap: {sonuc}")
        
        if hak_sayisi <= 0:
            print("\nKaybettiniz! Kelime:", kelime)
            break
            
        if "_" not in tahmin_kelime:
            print("\nTebrikler! Kelimeyi buldunuz:", kelime)
            break

        

def islem_kategori_sec():
    """İşlem türünü seçmek için kullanıcıdan giriş alır"""
    islem_turleri = ["toplama", "cikarma", "carpma", "bolme"]
     
    print("\nİşlem türünü seçiniz:")
    for islem in islem_turleri:
        print(f"[{islem}]", end=" ")
    print()
    
    while True:
        islem = input("İşlem türü: ").lower().strip()
        if islem in islem_turleri:
            return islem
        print("Geçersiz işlem! Lütfen listeden bir işlem seçin.")

def iki_sayi_al():
    """Kullanıcıdan iki sayı alır"""
    while True:
        try:
            sayi1 = float(input("Birinci sayıyı giriniz: "))
            sayi2 = float(input("İkinci sayıyı giriniz: "))
            return sayi1, sayi2
        except ValueError:
            print("Hatalı giriş! Lütfen sadece sayı giriniz.")

def islem_yap():
    """Matematik işlemlerini gerçekleştirir"""
    # İşlem türünü seç
    islem_turu = islem_kategori_sec()
    
    # İki sayıyı al
    sayi1, sayi2 = iki_sayi_al()
    
    # İşlemleri gerçekleştir
    if islem_turu == "toplama":
        sonuc = sayi1 + sayi2
        
    elif islem_turu == "cikarma":
        sonuc = sayi1 - sayi2
                
    elif islem_turu == "carpma":
        sonuc = sayi1 * sayi2      
        
    elif islem_turu == "bolme":
        if sayi2 == 0:
            print("\nHata: Sıfıra bölme işlemi yapılamaz!")
            return None
        sonuc = sayi1 / sayi2
   
    return sonuc




oyun()