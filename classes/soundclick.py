from base import *

class SoundClick(Media):
    def get_total_urls(self, sc_obj=None):
        config_objs = config.info["soundclick"]

        urls = []
        for keyword in config_objs.keys():
            value =  config_objs[keyword]
            url_keyword = value["url_keyword"]
            genre_id = value["genre_id"]

            # song url
            mark = 0
            url = "https://www.soundclick.com/genres/charts.cfm?genre={}&genreid={}&showonly={}&orderCharts=1&advstate=0&advcountry=0&advvip=0&advfeatured=0&advsigned=2".format(url_keyword, genre_id, mark)
            obj = {}
            obj["genre_id"] = genre_id
            obj["type"] = config.ROW_DATA_TYPE_SONG
            obj["url"] = url
            obj["total_pages"] = 0
            obj["keyword"] = url_keyword
            urls.append(obj)

            # signed url
            mark = 3
            url = "https://www.soundclick.com/genres/charts.cfm?genre={}&genreid={}&showonly={}&orderCharts=1&advstate=0&advcountry=0&advvip=0&advfeatured=0&advsigned=2".format(url_keyword, genre_id, mark)
            obj = {}
            obj["genre_id"] = genre_id
            obj["type"] = config.ROW_DATA_TYPE_SIGNED_BAND
            obj["url"] = url
            obj["total_pages"] = 0
            obj["keyword"] = url_keyword
            urls.append(obj)

            # unsigned url
            mark = 4
            url = "https://www.soundclick.com/genres/charts.cfm?genre={}&genreid={}&showonly={}&orderCharts=1&advstate=0&advcountry=0&advvip=0&advfeatured=0&advsigned=2".format(url_keyword, genre_id, mark)
            obj = {}
            obj["genre_id"] = genre_id
            obj["type"] = config.ROW_DATA_TYPE_UNSIGNED_BAND
            obj["url"] = url
            obj["total_pages"] = 0
            obj["keyword"] = url_keyword
            urls.append(obj)

        return urls

    def parse_all_urls(self, sc_obj, url_item):
        url = url_item["url"]

        self.set_proxy(sc_obj)
        
        total_no = 0
        stop_flag = False

        self.wait()
        # print url
        while stop_flag == False:
            agent_str = random_agent()[2]
            
            headers = {
                "Host": "www.soundclick.com",
                "User-Agent": agent_str,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
            }

            html = sc_obj.load(url, use_cache = False, headers=headers)
            error_code = self.check_proxy_status(html)

            if error_code == config.ERROR_NONE:
                last_page = html.q("//div[@class='pageturner']/a[contains(text(), 'last')]")
                
                if len(last_page) > 0:
                    last_page_url = last_page[0].x("@href").strip()
                    try:
                        total_no = int(re.search("currentPage=(.*)", last_page_url, re.I|re.S|re.M).group(1))
                        url_item["total_pages"] = total_no
                    except:
                        pass

                stop_flag = True
            else:
                self.set_proxy(sc_obj)
                self.wait()
                proxy_info = html.response.request.get("proxy")
                error_str = "proxy error in {}, {}, {}:{}".format(url, error_code, proxy_info.host, proxy_info.port)
                print error_str    

                global_sc_obj.save(["error", error_str], "error.csv")

        print "Genre = ", url_item["keyword"], ", Type = ", url_item["type"], ", Total Page =", total_no

    def parse_website(self, sa_db, sc_obj, url_item, total_urls):
        url_obj = url_item["item"]
        item = {}

        url = url_obj["url"]
        
        # print "*************************LEFT URL = ", len(total_urls)
        # print url
        item["type"] = url_obj["type"]

        item["genre_id"] = url_obj["genre_id"]
        item["rank_date"] = self.begin_time.strftime("%Y-%m-%d %H-%M-%S")
        item["source_site"] = self.class_name
        item["url"] = url

        html = sc_obj.load(url, use_cache = False)
        error_code = self.check_proxy_status(html)
        if error_code != config.ERROR_NONE:
            proxy_info = html.response.request.get("proxy")
            error_str = "proxy error in {}, {}, {}:{}".format(url, error_code, proxy_info.host, proxy_info.port)
            print error_str

            global_sc_obj.save(["error", error_str], "error.csv")
            url_item["status"] = "none"
            return

        div_objs = html.q("//div/div/div[contains(@id, 'ueberDiv')]")
        
        for div_item in div_objs:
            try:
                chart_pos_div = div_item.q(".//div[@class='chartsPos']")
                last_pos_div = div_item.q(".//div[@class='chartsLast']//text()").join(" ")

                try:
                    item["ranking"] = int(chart_pos_div[0].x("text()").strip())
                except:
                    item["ranking"] = 0

                try:
                    item["last_ranking"] = int(last_pos_div.replace("from", "").replace("#", ""))
                except:
                    item["last_ranking"] = 0
                
                img_div = div_item.q(".//div[@class='songPic']/a/img")
                item["img_url"] = img_div[0].x("@src").strip()

                artist_div = div_item.q(".//div[contains(@class, 'bandBox')]//a[@class='chartsArtist']")
                song_div = div_item.q(".//div[contains(@class, 'bandBox')]//a[@class='chartsSong']")

                item["artist_link"] = artist_div[0].x("@href").strip()

                item["name"] = ""
                item["song_artist_name"] = ""
                if item["type"] == config.ROW_DATA_TYPE_SONG:
                    item["name"] = song_div[0].x("text()").strip()
                    item["song_artist_name"] = artist_div[0].x("text()").strip()
                else:
                    item["name"] = artist_div[0].x("text()").strip()

                db_obj = None
                exist = False
                if item["type"] == config.ROW_DATA_TYPE_SONG:
                    db_obj = sa_db.session.query(Song).filter_by(name=item["name"], genre_id=item["genre_id"], 
                        song_artist_name =item["song_artist_name"], source_site=item["source_site"]).first()               

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

                # Signed and Unsigned Case
                else:
                    if item["type"] == config.ROW_DATA_TYPE_UNSIGNED_BAND: #unsigned part create
                        db_obj = sa_db.session.query(UnsignedBand).filter_by(name=item["name"], genre_id=item["genre_id"], 
                            source_site=item["source_site"]).first()               
                        
                        if db_obj == None:
                            db_obj = UnsignedBand(
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
                        else:
                            exist = True

                    else: #signed part create
                        db_obj = sa_db.session.query(SignedBand).filter_by(name=item["name"], genre_id=item["genre_id"], 
                            source_site=item["source_site"]).first()               

                        if db_obj == None: 
                            db_obj = SignedBand(
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

                        else: # Upate Part
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
                    self.show_exception_detail(e)
                    break

            except Exception as e:
                self.show_exception_detail(e)

        url_item["status"] = "complete"