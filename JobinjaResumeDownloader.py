import requests
from bs4 import BeautifulSoup
import os
import time
import json

csrf_token = None

def load_settings():
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        print("فایل config.json یافت نشد. لطفاً آن را ایجاد و مقادیر مورد نیاز را وارد کنید.")
        return None
    except json.JSONDecodeError:
        print("فرمت فایل config.json معتبر نیست. لطفاً آن را بررسی کنید.")
        return None

def save_html(html, filename="page.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML صفحه ذخیره شد: {filename}")

def download_resume(url, headers, output_folder):
    global csrf_token  
    try:

        headers = {
            'Cookie': f'{cookie}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept': '*/*',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'x-csrf-token': f'{csrf_token}',
            'x-requested-with': 'XMLHttpRequest',
            'Accept-Language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
            'Origin': 'https://panel.jobinja.ir',
            'Referer': f'https://panel.jobinja.ir/novaday/posts/{url.split("/")[-1]}'
        }

        data = f"_token={csrf_token}"
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_link = soup.find('a', {'data-action': 'click->download#download'})

            if download_link:
                download_link = download_link.get("href") 
                
                if download_link:
                    file_response = requests.get(download_link, headers=headers)
                    if file_response.status_code == 200:
                        file_name = os.path.join(output_folder, download_link.split("/")[-1].split("?")[0])  # نام فایل را از لینک بگیرید
                        with open(file_name, "wb") as f:
                            f.write(file_response.content)
                        print(f"فایل با موفقیت دانلود شد: {file_name}")
                    else:
                        print("دانلود فایل از لینک src با خطا مواجه شد.")
                else:
                    print("لینک href در a پیدا نشد.")
            else:
                print("a با مشخصات مشخص‌شده یافت نشد.")


        else:
            print(f"خطا در دانلود رزومه: {url} - وضعیت {response.status_code}")
    except Exception as e:
        print(f"خطا در دانلود رزومه {url}: {e}")

def process_pages(cookie, jsessid, xsrf_token, company_name,job_ad_id, max_pages=5, delay=2):
    global csrf_token  
    base_url = f"https://panel.jobinja.ir/{company_name}/posts/{job_ad_id}?page="
    headers = {
        "Cookie": f'{cookie}',
        "sec-fetch-site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    output_folder = "resumes"
    os.makedirs(output_folder, exist_ok=True)

    for page in range(1, max_pages + 1):
        print(f"در حال پردازش صفحه {page}...")
        print(base_url + str(page))
        response = requests.get(base_url + (str(page) if page > 1 else ""), headers=headers)
        if response.status_code != 200:
            print(f"خطا در دریافت صفحه {page}: وضعیت {response.status_code}")
            break
        
        save_html(response.text, f"page_{page}.html")
        
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr", {"data-candidate-box-url": True})

        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
        print(f"CSRF Token به‌روزرسانی شد: {csrf_token}")

        if not rows:
            print(f"هیچ لینکی در صفحه {page} یافت نشد. ممکن است ساختار سایت تغییر کرده باشد.")
            break

        resume_links = [row["data-candidate-box-url"] for row in rows]
        if not resume_links:
            print(f"هیچ رزومه‌ای در صفحه {page} یافت نشد.")
            break
        
        for link in resume_links:
            download_resume(link, headers, output_folder)
        
        time.sleep(delay)
    
    print("عملیات به پایان رسید.")

if __name__ == "__main__":
    settings = load_settings()
    if not settings:
        exit()

    cookie = settings.get("COOKIE")
    jsessid = settings.get("JSESSID")
    xsrf_token = settings.get("XSRF-TOKEN")
    company_name = settings.get("company_name")
    job_ad_id = settings.get("job_ad_id")
    max_pages = settings.get("max_pages", 5)
    delay = settings.get("delay", 2)

    if not cookie or not jsessid or not xsrf_token or not company_name:
        print("برخی از مقادیر ضروری (COOKIE, JSESSID، XSRF-TOKEN، نام شرکت) در فایل تنظیمات وارد نشده است.")
    else:
        process_pages(cookie, jsessid, xsrf_token, company_name,job_ad_id, max_pages, delay)
