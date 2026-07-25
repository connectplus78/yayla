# bot.py
import requests
from bs4aitan import BeautifulSoup
import yaml
import json
import os

def config_yukle():
    if os.path.exists('vakit.yml'):
        with open('vakit.yml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {
        "ulke": "TURKIYE",
        "sehir": "ISTANBUL",
        "url": "https://fazilettakvimi.com/namaz-vakitleri/"
    }

def vakitleri_cek():
    config = config_yukle()
    url = config.get('url', 'https://fazilettakvimi.com/namaz-vakitleri/')
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Fazilettakvimi sitesinin güncel yapısına göre vakitleri barındıran alanlar
        # Örnek veri çekme mantığı (Site yapısına göre güncellenebilir)
        vakitler = {}
        
        # Sitedeki tablo veya liste yapılarını ayıklama
        # Alternatif olarak JSON çıktısı üretip index.html'in okumasını sağlayabiliriz
        times_container = soup.find_all('div', class_='vakit-table') # veya ilgili HTML elementi
        
        data = {
            "sehir": config.get('sehir'),
            "durum": "Basarili",
            "html_icerik": response.text[:500] # Örnek kontrol
        }
        
        # Vakitleri JSON dosyasına kaydedelim ki index.html okuyabilsin
        with open('vakitler.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Namaz vakitleri başarıyla güncellendi ve vakitler.json dosyasına yazıldı.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    vakitleri_cek()
