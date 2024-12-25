from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import json, re
import pandas as pd
from to_mysql import db_config, conn, cursor
from to_mysql import insert_profile_target, insert_profile_user
from crawl_post import get_number

def crawl_profile(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()
        print(f"Going to page: {url}")
        page.goto(url)
        time.sleep(3)  

        soup = BeautifulSoup(page.content(), 'html.parser')

        cover_image_tag = soup.find('img', {'data-imgperflogname': 'profileCoverPhoto'})
        cover_image = cover_image_tag['src'] if cover_image_tag else "none"

        logo_image_tag = soup.select_one('g image')
        logo_image = logo_image_tag['xlink:href'] if logo_image_tag else "none"

        num_like_tag = soup.find('a', string=re.compile(r' thích$'))
        num_like = get_number(num_like_tag.get_text()) if num_like_tag else 0

        num_follower_tag = soup.find('a', string=re.compile(r' người theo dõi$'))
        num_follower = get_number(num_follower_tag.get_text()) if num_follower_tag else 0

        num_following_tag  = soup.find('a', string=re.compile(r' đang theo dõi$'))
        num_following = get_number(num_following_tag.get_text()) if num_following_tag else 0

        photo = soup.find_all('div', class_='x1yztbdb')[1]
        photos = [img['src'] for img in photo.select('img')]
        
        detail = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else "none"

        data = {
            'url': url,
            'cover_image': cover_image,
            'logo_image': logo_image,
            'num_like': num_like,
            'num_follower': num_follower,
            'num_following': num_following,
            'detail': detail,
            'post_photos': photos
        }

        insert_profile_target(url, cover_image, logo_image, num_like, num_follower, num_following, detail, None)

        print(f"Finished scraping {url}")
        page.close()

        browser.close()
def crawl_user(entry_url, get_url_window):
    url = entry_url.get()
    url = f"{url}"
    print(url)
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        page = context.new_page()
        print(f"Going to page: {url}")
        page.goto(url)
        time.sleep(3)  

        soup = BeautifulSoup(page.content(), 'html.parser')

        cover_image_tag = soup.find('img', {'data-imgperflogname': 'profileCoverPhoto'})
        cover_image = cover_image_tag['src'] if cover_image_tag else "none"

        logo_image_tag = soup.select_one('g image')
        logo_image = logo_image_tag['xlink:href'] if logo_image_tag else "none"

        num_like_tag = soup.find('a', string=re.compile(r' thích$'))
        num_like = get_number(num_like_tag.get_text()) if num_like_tag else 0

        num_follower_tag = soup.find('a', string=re.compile(r' người theo dõi$'))
        num_follower = get_number(num_follower_tag.get_text()) if num_follower_tag else 0

        num_following_tag  = soup.find('a', string=re.compile(r' đang theo dõi$'))
        num_following = get_number(num_following_tag.get_text()) if num_following_tag else 0

        photo = soup.find_all('div', class_='x1yztbdb')[1]
        photos = [img['src'] for img in photo.select('img')]
        
        detail = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else "none"

        data = {
            'url': url,
            'cover_image': cover_image,
            'logo_image': logo_image,
            'num_like': num_like,
            'num_follower': num_follower,
            'num_following': num_following,
            'detail': detail,
            'post_photos': photos
        }

        insert_profile_user(url, cover_image, logo_image, num_like, num_follower, num_following, detail, None)

        print(f"Finished scraping {url}")
        page.close()

        browser.close()
    get_url_window.destroy()