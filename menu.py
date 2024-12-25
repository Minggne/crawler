import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
from playwright.sync_api import sync_playwright
import os
import time
import re
from bs4 import BeautifulSoup
from crawl_post import get_number
from crawl_profile import crawl_user
from handle_data import return_profile_user
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from crawl_post import implement
from handle_data import get_post_info, filter_keyword
from to_mysql import db_config, conn, cursor



def show_main_menu():
    account_name, followers_count = return_profile_user()[0]
    account_name = account_name.split('/')[-1]

    main_window = tk.Tk()
    main_window.title("Facebook Scraper")
    main_window.geometry("1000x700")
    main_window.configure(bg="#121212")

    header_font = Font(family="Arial", size=16, weight="bold")
    label_font = Font(family="Arial", size=12)

    frame_header = tk.Frame(main_window, bg="#1E1E1E")
    frame_header.pack(fill="x", pady=10)

    greeting_label = tk.Label(frame_header, text=f"Xin chào, {account_name}", font=header_font, fg="#FFFFFF", bg="#1E1E1E")
    greeting_label.pack(side="left", padx=10)

    followers_label = tk.Label(frame_header, text=f"Số người theo dõi: {followers_count}", font=label_font, fg="#F39C12", bg="#1E1E1E")
    followers_label.pack(side="right", padx=10)

    frame_url = tk.Frame(main_window, bg="#121212")
    frame_url.pack(fill="x", pady=10)

    tk.Label(frame_url, text="URL Page:", font=label_font, fg="#FFFFFF", bg="#121212").grid(row=0, column=0, padx=10, pady=5)
    entry_url = tk.Entry(frame_url, width=50, font=("Arial", 12))
    entry_url.grid(row=0, column=1, padx=10, pady=5)

    # bắt đầu crawl
    def scrape_action():
        url_page = entry_url.get()
        messagebox.showinfo("Thông báo", f"Bắt đầu thu thập dữ liệu từ {url_page}...")
        implement(url_page)
        data = get_post_info(url_page)
        
        for post in data:
            tree.insert("", "end", values=post)
    def tool_action(keyword):
        def get_selected_option():
            if like_var.get():
                return "likes"
            elif share_var.get():
                return "shares"
            elif like_var.get():
                return "comments"
            else:
                return "likes"
        # Xóa tất cả các dòng trong Treeview
        for item in tree.get_children():
            tree.delete(item)

        data = filter_keyword(get_selected_option(), "DESC", 10, keyword)
        for post in data:
            tree.insert("", "end", values=post)
    def on_check_change(*args):
    # Xử lý khi một checkbox được chọn
        if like_var.get():
            # Khi "Like" được chọn, bỏ chọn "Share" và "Comment"
            share_var.set(False)
            comment_var.set(False)
        elif share_var.get():
            # Khi "Share" được chọn, bỏ chọn "Like" và "Comment"
            like_var.set(False)
            comment_var.set(False)
        elif comment_var.get():
            # Khi "Comment" được chọn, bỏ chọn "Like" và "Share"
            like_var.set(False)
            share_var.set(False)

    btn_scrape = tk.Button(frame_url, text="Bắt đầu thu thập dữ liệu", font=("Arial", 12), bg="#F39C12", fg="#FFFFFF", command=scrape_action)
    btn_scrape.grid(row=0, column=2, padx=10, pady=5)

    frame_main = tk.Frame(main_window, bg="#121212")
    frame_main.pack(fill="both", expand=True, pady=10)

    frame_tools = tk.Frame(frame_main, width=200, bg="#1E1E1E")
    frame_tools.pack(side="left", fill="y", padx=10, pady=10)

    frame_results = tk.Frame(frame_main, bg="#121212")
    frame_results.pack(side="right", fill="both", expand=True)

    columns = ("Post ID", "Post Content", "Likes", "Shares", "Comments", "Date")
    tree = ttk.Treeview(frame_results, columns=columns, show="headings", style="Custom.Treeview")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview", background="#1E1E1E", foreground="#FFFFFF", rowheight=25, fieldbackground="#1E1E1E", font=("Arial", 12))
    style.map("Custom.Treeview", background=[("selected", "#F39C12")])

    tk.Label(frame_tools, text="Tools", font=("Arial", 14, "bold"), fg="#FFFFFF", bg="#1E1E1E").pack(pady=10)

    like_var = tk.BooleanVar()
    like_var.trace_add("write", on_check_change)
    tk.Checkbutton(frame_tools, text="Like", variable=like_var, bg="#1E1E1E", fg="#FFFFFF", selectcolor="#1E1E1E", font=label_font, command=lambda: tool_action("")).pack(anchor="w", padx=10, pady=5)

    share_var = tk.BooleanVar()
    share_var.trace_add("write", on_check_change)
    tk.Checkbutton(frame_tools, text="Share", variable=share_var, bg="#1E1E1E", fg="#FFFFFF", selectcolor="#1E1E1E", font=label_font, command=lambda: tool_action("")).pack(anchor="w", padx=10, pady=5)

    comment_var = tk.BooleanVar()
    comment_var.trace_add("write", on_check_change)
    tk.Checkbutton(frame_tools, text="Comment", variable=comment_var, bg="#1E1E1E", fg="#FFFFFF", selectcolor="#1E1E1E", font=label_font, command=lambda: tool_action("")).pack(anchor="w", padx=10, pady=5)

    tk.Label(frame_tools, text="Tìm kiếm:", bg="#1E1E1E", fg="#FFFFFF", font=label_font).pack(anchor="w", padx=10, pady=5)
    keyword_entry = tk.Entry(frame_tools, width=20, font=("Arial", 12))
    keyword_entry.pack(anchor="w", padx=10, pady=5)
    search_button = tk.Button(frame_tools, text="Tìm kiếm", font=("Arial", 12), bg="#F39C12", fg="#FFFFFF", command=lambda: tool_action(keyword_entry.get()))
    search_button.pack(anchor="w", padx=10, pady=10)

    
    main_window.mainloop()


if __name__ == "__main__":
    show_main_menu()