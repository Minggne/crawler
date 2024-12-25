from playwright.sync_api import sync_playwright
import time
import tkinter as tk
from tkinter import messagebox
from crawl_profile import crawl_user
from handle_data import return_profile_user
from menu import show_main_menu

login_window = tk.Tk()
login_window.title("Đăng nhập Facebook")

def handle_facebook(entry_email, entry_password):
    us = entry_email.get()
    ps = entry_password.get()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Chạy ở chế độ hiển thị
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.facebook.com/")
        
        # Điền email và mật khẩu của bạn
        page.fill("input[name='email']", us)
        page.fill("input[name='pass']", ps)
        page.click("button[name='login']")
        
        # Đợi đăng nhập hoàn tất
        time.sleep(20)

        # Lưu trạng thái đăng nhập để tái sử dụng
        context.storage_state(path="fb_login_state.json")
        print("Đã đăng nhập hoàn tất!")
        time.sleep(5)

        browser.close()
    get_user_profile()
          
def login_form():
    # login_window = tk.Tk()
    # login_window.title("Đăng nhập Facebook")

    frame_login = tk.Frame(login_window)
    frame_login.pack(pady=20)

    tk.Label(frame_login, text="Email:").grid(row=0, column=0, padx=5, pady=5)
    entry_email = tk.Entry(frame_login, width=30)
    entry_email.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_login, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(frame_login, width=30, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    btn_login = tk.Button(frame_login, text="Đăng nhập", command=lambda: handle_facebook(entry_email, entry_password))
    btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    login_window.mainloop()

def get_user_profile():
    global frame_data

    login_window.destroy()
    get_url_window = tk.Tk()
    get_url_window.title("Scrapping your profile")

    frame_main = tk.Frame(get_url_window)
    frame_main.pack(pady=10)

    tk.Label(frame_main, text="URL Profile:").grid(row=1, column=0, padx=5, pady=5)
    entry_url = tk.Entry(frame_main, width=50)
    entry_url.grid(row=1, column=1, padx=5, pady=5)

    btn_scrape = tk.Button(frame_main, text="Thu thập dữ liệu", command=lambda:crawl_user(entry_url, get_url_window))
    btn_scrape.grid(row=2, column=0, columnspan=2, pady=10)

    get_url_window.mainloop()
    # print(return_profile_user())
    show_main_menu()

login_form()

# user_profile = https://www.facebook.com/profile.php?id=100084793945475
# page_ = https://www.facebook.com/ctsvdhbkdhdn