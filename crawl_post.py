from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import json, re
import pandas as pd
import pyperclip
from to_xlsx import to_xlsx
from to_mysql import insert_post

# url="https://www.facebook.com/ctsvdhbkdhdn"

# link_post, id_post, time_post, time_crawl, thumbnail_video

all_data = []
post_list = []
profile_data = []
# url_page = "https://www.facebook.com/ctsvdhbkdhdn"
# url_page = "https://www.facebook.com/ctsvdhbkdhdn"

def get_number(text):
    number = int(re.search(r'\d+', text).group())
    return number

def scroll_down(page, num):
    for _ in range(num):
        # page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        page.evaluate("window.scrollBy(0, 1200);")
        time.sleep(3)

def get_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return current_time

def select_info_post(soup, url_page):
    posts = soup.find_all('div', {'data-ad-preview': 'message'})
    post_stt = 1
    for post in posts:
        post_content = post.get_text(strip=True)

        # html-div chứa bài viết
        div_parent = post.find_parent("div", {"class": "html-div"}).find_parent().find_parent().find_parent()

        # crawl reaction
        span_tag = div_parent.find("span", attrs={
            "aria-label": lambda label: label in [
                "Xem ai đã bày tỏ cảm xúc về tin này",
                "See who reacted to this"
            ]
        })

        par_span_tag = span_tag.find_parent()

        span = par_span_tag.find("span", {"aria-hidden": "true"})

        like_span = span.find("span").find("span")
        if like_span:
            like_count = like_span.get_text()
            like_count = get_number(like_count)
        else:
            like_count = 0

        # crawl cmt + share
        cmt_div = span_tag.find_parent("div", {"class": "x1n2onr6"})
        next_cmt_div = cmt_div.find("div")
        span_html = next_cmt_div.find_all("span", {"class": "html-span"})

        if (not span_html):
            comment_count = 0
            share_count = 0

        else: 
            if len(span_html) < 2:
                text = span_html[0].get_text()
                if "bình luận" in text:
                    comment_count = text
                    comment_count = get_number(text)
                    share_count = 0
                if "chia sẻ" in text:
                    share_count = text
                    share_count = get_number(text)
                    comment_count = 0
            else:
                comment_count = span_html[0].get_text()
                comment_count = get_number(comment_count)
                share_count = span_html[1].get_text()
                share_count = get_number(share_count)

        # link post
        html_contain_link = div_parent.find_all("div", {"class": "html-div"})[0]
        div_contain_a = html_contain_link.find_all("div", {"class": "xu06os2 x1ok221b"})[1]
        a_tag = div_contain_a.find("a")
        link_post = a_tag.get("href")

        # link hinh anh
        div_contain_post_content = post.find_parent("div", {"class": "html-div"}).find_parent().find_parent()
        div_2nd = div_contain_post_content.find_all("div", {"class": "html-div"})[2]

        img_tag = div_2nd.find("img")

        if img_tag:
            img_link = img_tag.get("src")
        else: 
            img_link = "N/A" 

        collected_time = get_time()
        # lưu vào all_data
        all_data.append(
            {
                "post_id": post_stt,
                "post_content": post_content,
                "link_post": link_post,
                "link_img": img_link,
                "likes": like_count,
                "comments": comment_count,
                "shares": share_count,
                "collected_time": collected_time,
                "page_url" : url_page
            }
        )

        insert_post(post_content, link_post, img_link, like_count, comment_count, share_count, collected_time, url_page)
        post_stt = post_stt + 1
        time.sleep(2)

def crawl_num(page, so_lan, url_page):
    # lần đầu 2 bài
    # scroll_down(page, 1)
    soup = BeautifulSoup(page.content(), 'html.parser')
    select_info_post(soup, url_page)

    for i in range(so_lan):
        print("----")

        # lần sau 5 bài
        scroll_down(page, 3)
        soup = BeautifulSoup(page.content(), 'html.parser')
        select_info_post(soup, url_page)

def implement(url_page):
    with sync_playwright() as p:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="fb_login_state.json", user_agent=user_agent)

        page = context.new_page()
        
        print(f"Going to page: {url_page}")
        page.goto(url_page)
        time.sleep(3)

        crawl_num(page, 2, url_page)
        page.close()
        browser.close()
