from base import *
from sqlalchemy import text

class SoundCloud(Media):
    def get_total_urls(self, sc_obj=None):

        html = sc_obj.load("https://soundcloud.com/charts",  use_cache = False)
        # with open("response.html", 'w') as f:
        #     f.write(html.encode("utf8"))
        #     print html
        
        # return
        genre_list = html.q("//section[@class='categories']/article")

        # print len(genre_list)

        for genre in genre_list:
            h2_str = genre.q("h2[contains(text(), 'Choose a genre')]")

            if len(h2_str) > 0:
                articles = genre.q(".//ul/li")

                for i , article in enumerate(articles):
                    if i > 1:
                        genre_str = article.x("a/text()")
                        href_link =  article.x("a/@href")
                        genre_link = re.search("genre=(.*)", href_link, re.I|re.S|re.M).group(1)                        
                        
                        config.info[self.class_name][genre_str] = {"url_keyword": genre_link, "genre_id":0}

        config_objs = config.info[self.class_name]

        urls = []
        for keyword in config_objs.keys():

            value =  config_objs[keyword]
            url_keyword = value["url_keyword"]
            genre_id = value["genre_id"]

            # song url
            client_id = "OmTFHKYSMLFqnu2HHucmclAptedxWXkq"
            app_version = "1507542500"
            offset = 0
            limit = 100

            url = "https://api-v2.soundcloud.com/charts?genre=soundcloud:genres:{}&offset={}&high_tier_only=false&kind=top&limit={}&client_id={}&app_version={}".format(url_keyword, offset, limit, client_id, app_version)
            
            obj = {}
            obj["genre_id"] = genre_id
            obj["type"] = config.ROW_DATA_TYPE_SONG
            obj["url"] = url
            obj["total_pages"] = 0
            obj["keyword"] = url_keyword
            urls.append(obj)

        return urls

    def parse_website(self, sa_db, sc_obj, url_item, total_urls):
        url_obj = url_item["item"]
        item = {}

        url = url_obj["url"]

        print "*************************LEFT URL = ", len(total_urls)
        print url

        item["type"] = url_obj["type"]

        item["genre_id"] = url_obj["genre_id"]
        item["rank_date"] = self.begin_time.strftime("%Y-%m-%d %H-%M-%S")
        item["source_site"] = self.class_name
        item["url"] = url

        json_obj = sc_obj.load_json(url, use_cache = False)
        # error_code = self.check_proxy_status(html)

        # print "Error Code = ", error_code
        # if error_code != config.ERROR_NONE:
        #     proxy_info = html.response.request.get("proxy")
        #     error_str = "proxy error in {}, {}, {}:{}".format(url, error_code, proxy_info.host, proxy_info.port)
        #     print error_str

        #     global_sc_obj.save(["error", error_str], "error.csv")
        #     url_item["status"] = "none"
        #     return

        if json_obj == None:
            print "Data does not exist ->", url
            url_item["status"] = "complete"
            return

        collections = json_obj["collection"]
        # print "Len=", len(collections)

        for i, collection in enumerate(collections):

            try:
                item["ranking"] = i + 1
                item["last_ranking"] = i + 1

                item["img_url"] = collection["track"]["artwork_url"]

                if item["img_url"] == None:
                    item["img_url"] = collection["track"]["user"]["avatar_url"]

                item["artist_link"] = collection["track"]["user"]["permalink_url"]

                item["name"] = ""
                item["song_artist_name"] = ""

                if item["type"] == config.ROW_DATA_TYPE_SONG:
                    title_str = collection["track"]["title"]
                    artist_name_str = collection["track"]["user"]["username"]

                    item["name"] = title_str
                    item["song_artist_name"] = artist_name_str

                db_obj = None
                exist = False
                if item["type"] == config.ROW_DATA_TYPE_SONG:
                    db_obj = sa_db.session.query(Song).filter_by(name=item["name"], song_artist_name =item["song_artist_name"], source_site=item["source_site"]).first()

                    if db_obj == None:
                        db_obj = Song(
                            ranking = item["ranking"],
                            last_ranking = item["last_ranking"], 
                            image_link = item["img_url"], 
                            name = item["name"], 
                            song_artist_name = item["song_artist_name"],
                            artist_page_link = item["artist_link"], 
                            genre_id = item["genre_id"], 
                            rank_date = item["rank_date"], 
                            source_site = item["source_site"]
                        )
                    else:   # Upate Part
                        exist = True

                try:
                    if exist == False:
                        sa_db.session.add(db_obj)

                    else:
                        db_obj.ranking = item["ranking"]
                        db_obj.last_ranking = item["last_ranking"]
                        db_obj.image_link = item["img_url"]
                        db_obj.artist_page_link = item["artist_link"]
                        db_obj.song_artist_name = item["song_artist_name"]
                        db_obj.rank_date = item["rank_date"]
                    
                    sa_db.session.commit()

                except Exception as e:
                    sa_db.session.rollback()
                    print item["name"], item["song_artist_name"]
                    # self.show_exception_detail(e)
                    # break

            except Exception as e:
                self.show_exception_detail(e)

        url_item["status"] = "complete"
