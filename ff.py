import requests
from bs4 import BeautifulSoup
import os

def fetch_obfs4_bridges():
    """گرفتن پل‌های obfs4 از BridgeDB"""
    try:
        url = "https://bridges.torproject.org/bridges?transport=obfs4"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }
        print(f"در حال ارسال درخواست به: {url} با هدر: {headers}")
        response = requests.get(url, headers=headers, timeout=20)
        print(f"کد وضعیت: {response.status_code}")
        print(f"پاسخ کامل (1000 کاراکتر اول): {response.text[:1000]}")
        
        if response.status_code == 200:
            # پردازش HTML با BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            bridge_div = soup.find('div', id='bridgelines')
            if bridge_div:
                # گرفتن تمام خطوط داخل div
                lines = bridge_div.get_text().splitlines()
                # فیلتر کردن خطوطی که با obfs4 شروع می‌شن
                bridges = [line.strip() for line in lines if line.strip().startswith("obfs4")]
                if bridges:
                    print(f"پل‌های دریافت‌شده: {bridges}")
                    return bridges
                else:
                    print("هیچ پل obfs4 پیدا نشد! ممکنه ساختار HTML عوض شده باشه.")
                    return None
            else:
                print("تگ <div id='bridgelines'> پیدا نشد!")
                return None
        else:
            print(f"خطا در اتصال به BridgeDB: {response.status_code}, پاسخ: {response.text[:1000]}")
            return None
    except Exception as e:
        print(f"خطا در گرفتن پل‌ها: {str(e)}")
        return None

def save_bridges_to_file(bridges, output_file="bridges.txt"):
    """ذخیره پل‌ها در فایل"""
    if bridges:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for bridge in bridges:
                    f.write(f"{bridge}\n")
            print(f"پل‌ها در {output_file} ذخیره شدند.")
            return True
        except Exception as e:
            print(f"خطا در ذخیره پل‌ها: {str(e)}")
            return False
    return False

if __name__ == "__main__":
    bridges = fetch_obfs4_bridges()
    if bridges:
        save_bridges_to_file(bridges)
    else:
        print("نمی‌تونم پل‌ها رو ذخیره کنم!")
