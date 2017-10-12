from scrapex import *
import time
import config
from datetime import datetime
from datetime import date
from time import sleep
import random, re, os, sys
from proxy_list import random_proxy
from time import gmtime, strftime
from datetime import datetime
from logging import exception
import os
from scrapex.http import Proxy
import json
from models import *
from agent import random_agent

global_sc_obj = Scraper(
    use_cache=False, #enable cache globally
    retries=3, 
    timeout=60,
    )

class Media:
    def __init__(self, class_name, rand_sc, rand_sa_db):
        self.class_name = class_name
        self.begin_time = datetime.now()
        self.page_error = config.ERROR_NONE
        self.rand_sc = rand_sc
        self.rand_sa_db = rand_sa_db

    # Show details of exception error
    def show_exception_detail(self, e):
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("{}, {}, {}".format(exc_type, fname, str(exc_tb.tb_lineno)))

    # Note proxy problems
    def check_proxy_status(self, html):
        error_code = config.ERROR_NONE

        # Error with proxy
        if html.response.code == 0 or html.response.code == 503:
            error_code = config.ERROR_PROXY_PROVIDER
        # Site refused proxy
        elif html.response.code == 403 or html.response.code == 400:
            error_code = config.ERROR_403_400
        # 500 Internal Server Error
        elif html.response.code == 500:
            error_code = config.ERROR_INTERNAL_SERVER

        return error_code
    
    def set_proxy(self, sc_obj):
        proxy_ip, proxy_port, proxy_user, proxy_pass = random_proxy()

        auth_str = "{}:{}".format(proxy_user, proxy_pass)
        proxy = Proxy(proxy_ip, proxy_port, auth_str)

        sc_obj.proxy_manager.session_proxy = proxy


    def check_proxy_ip(self, scrape_obj):
        html = scrape_obj.load_json("http://lumtest.com/myip.json", use_cache=False)
        scrape_obj.info(html["ip"])

    # Wait a random amount of time before entering values
    def wait(self):
        random_time = random.randrange(config.DRIVER_SHORT_WAITING_SECONDS, config.DRIVER_MEDIUM_WAITING_SECONDS)
        print "Sleep Time = ", random_time
        sleep(random_time)

    def get_total_urls(self):
        pass

    def parse_website(self, sa_db, sc_obj, url_obj, total_urls):
        pass

    def parse_all_urls(self, sc_obj, url_item):
        pass

    def save_genre(self):
        pass