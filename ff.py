import requests
import os

def fetch_obfs4_bridges():
    """گرفتن پل‌های obfs4 از BridgeDB"""
    try:
        url = "https://bridges.torproject.org/bridges?transport=obfs4"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            bridges = [line.strip() for line in response.text.splitlines() if line.startswith("obfs4")]
            if bridges:
                return bridges
            else:
                print("هیچ پل obfs4 پیدا نشد!")
                return None
        else:
            print(f"خطا در اتصال به BridgeDB: {response.status_code}")
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
