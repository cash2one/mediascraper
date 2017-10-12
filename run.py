from classes import *
import mysql_manage as db
import config
import sys
import argparse
from proxy_list import random_proxy
from scrapex import *
from scrapex import common
from scrapex.node import Node
from scrapex.excellib import *
from scrapex.http import Proxy

# DB
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.mysql_connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.sa_track_mods

def set_proxy(sc_obj):
    proxy_ip, proxy_port, proxy_user, proxy_pass = random_proxy()

    auth_str = "{}:{}".format(proxy_user, proxy_pass)
    proxy = Proxy(proxy_ip, proxy_port, auth_str)

    sc_obj.proxy_manager.session_proxy = proxy

def custom_total_urls(mode, urls):
    total_urls = []
    print "Generating URLS..."
    for url_item in urls:
        total_urls.append({
            "item": {
                "url": url_item["url"],
                "type": url_item["type"],
                "genre_id": url_item["genre_id"]
            }, 
            "status":"none"})

        if mode == config.WEBSITE_SOUND_CLICK:
            if url_item["total_pages"] == 0:
                url_item["total_pages"] = 5
            
            for page_no in range(2, url_item["total_pages"]+1):
                url = url_item["url"] + "&currentPage=" + str(page_no)
                
                total_urls.append({
                    "item": {
                        "url": url,
                        "type": url_item["type"],
                        "genre_id": url_item["genre_id"]
                    }, 
                    "status":"none"})

    return total_urls

def start_scraping(threads_number, mode):
    global config

    threads = []
    sc_obj_list = []
    db_obj_list = []
    sa_db_list = []

    for i in range(0, threads_number):
        sc_obj = Scraper(
            use_cache=False, #enable cache globally
            timeout=120,
            retries=3
            )

        sc_obj_list.append(sc_obj)

        sa_db = SQLAlchemy(app)
        sa_db_list.append(sa_db)

    total_urls = []
    urls = []

    class_obj = None
    random_sc = random.choice(sc_obj_list)
    random_sa_db = random.choice(sa_db_list)

    if mode == config.WEBSITE_SOUND_CLICK:
        class_obj = SoundClick("soundclick", random_sc, random_sa_db)
    elif mode == config.WEBSITE_SOUND_CLOUD:
        class_obj = SoundCloud("soundcloud", random_sc, random_sa_db)

    urls = class_obj.get_total_urls()
    
    print "Calculating Total Pages..."
    print "Len = ", len(urls)

    for url in urls:
        sc_obj = random.choice(sc_obj_list)
        set_proxy(sc_obj)
        class_obj.parse_all_urls(sc_obj, url)
    
    total_urls = custom_total_urls(mode, urls)

    total_urls = [total_urls[0]]

    print "Start..."
    while True:
        while len(total_urls) > 0:
            if len(threads) < threads_number:
                url_obj = None
                
                for item in total_urls:
                    if item["status"] == "complete":
                        total_urls.remove(item)
                    elif item["status"] == "none":
                        url_obj = item
                        url_obj["status"] = "pending"
                        break

                if url_obj == None:
                    continue

                sc_obj = sc_obj_list[len(total_urls) % threads_number]
                sa_db = sa_db_list[len(total_urls) % threads_number]

                set_proxy(sc_obj)
                thread_obj = threading.Thread(target=class_obj.parse_website,
                                              args=(sa_db, sc_obj, url_obj, total_urls))
                threads.append(thread_obj)
                thread_obj.start()

            for thread in threads:
                if not thread.is_alive():
                    thread.join()
                    threads.remove(thread)

        if len(total_urls) == 0:
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Do something.")
    parser.add_argument('-t', '--threads', type=int, required=False,  default=1, help='Number of threads')
    parser.add_argument('-m', '--mode', type=str, required=False, default=0, help='Website Mode: 0->soundclick, 1->soundcloud')
    
    args = parser.parse_args()
    
    threads_number = args.threads
    website_mode = args.mode

    start_scraping(threads_number, int(website_mode))
