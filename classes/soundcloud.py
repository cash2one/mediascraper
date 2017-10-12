from base import *
from sqlalchemy import text

class SoundCloud(Media):
	def save_genre(self):
		config_info = config.info[self.class_name]
		root_url = config_info["root"]

		print "Try to get genre list in {}".format(root_url)
		
		html = self.rand_sc.load("{}/charts".format(root_url), use_cache=False)
		error_code = self.check_proxy_status(html)

		total_genres = 0
		if error_code == config.ERROR_NONE:
			genre_list = html.q("//section[@class='categories']/article")

			skip_flag = False
			for genre in genre_list:
				if skip_flag == True:
					break

				h2_str = genre.q("h2[contains(text(), 'Choose a genre')]")
				
				if len(h2_str) > 0:
					articles = genre.q(".//ul/li")

					for i , article in enumerate(articles):
						if i > 1:
							genre_name = article.x("a/text()")
							href_link =  article.x("a/@href")
							url_keyword = re.search("genre=(.*)", href_link, re.I|re.S|re.M).group(1)                        
							
							if genre_name == "Audiobooks" or genre_name == "Business":
								skip_flag = True
								break

							db_obj = self.rand_sa_db.session.query(Genre).filter_by(genre_name=genre_name, source_site=self.class_name).first()

							if db_obj == None: 
								db_obj = Genre(
										genre_name = genre_name,
										genre_url_keyword = url_keyword,
										source_site = self.class_name,
									)

								self.rand_sa_db.session.add(db_obj)

							else:
								db_obj.genre_name = genre_name
								db_obj.genere_url_keyword = url_keyword
								db_obj.source_site = self.class_name

							self.rand_sa_db.session.commit()

							total_genres += 1

		print "{} genres saved".format(total_genres)
		print "***************** Completed *****************"

	def get_total_urls(self):

		db_obj = list(self.rand_sa_db.session.query(Genre).filter_by(source_site=self.class_name).all())

		print "Genre List = ", len(db_obj)
		if len(db_obj) == 0:
			self.save_genre()

		config_info = config.info[self.class_name]
		root_url = config_info["root"]

		site_obj = {}
		for db_item in db_obj:

			genre_name = db_item.genre_name
			genre_id = db_item.genre_id
			url_keyword = db_item.genre_url_keyword

			site_obj[genre_name] = {
				"url_keyword": url_keyword,
				"genre_id": genre_id
			}

		urls = []
		for keyword in site_obj.keys():
			value =  site_obj[keyword]
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

		url = "https://api-v2.soundcloud.com/charts?genre=soundcloud:genres:pop&offset=0&high_tier_only=false&kind=top&limit=100&client_id=OmTFHKYSMLFqnu2HHucmclAptedxWXkq&app_version=1507542500"
		try:
			json_obj = sc_obj.load_json(url, use_cache = False)
		except:
			url_item["status"] = "none"
			return
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
		
		total_count = 0
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
					title_str = collection["track"]["title"].encode("utf-8")
					artist_name_str = collection["track"]["user"]["username"].encode("utf-8")
					
					title_convert_str = ""
					artist_convert_str = ""

					title_str = unicode(title_str, "utf-8")
					artist_name_str = unicode(artist_name_str, "utf-8")

					title_convert_str = re.sub(ur"[^\u0000\u0000-\uffff\uffff]", "", title_str, flags=re.UNICODE)
					artist_convert_str = re.sub(ur"[^\u0000\u0000-\uffff\uffff]", "", artist_name_str, flags=re.UNICODE)

					if (title_str != title_convert_str) or (artist_name_str != artist_convert_str):

						global_sc_obj.save([
							"type", "",
							"string", "******************",
							], "log.csv");

						global_sc_obj.save([
							"type", "origin song name",
							"string", title_str,
							], "log.csv");
						global_sc_obj.save([
							"type", "fixed song name",
							"string", title_convert_str,
							], "log.csv");
						global_sc_obj.save([
							"type", "original artist name",
							"string", artist_name_str,
							], "log.csv");
						global_sc_obj.save([
							"type", "fixed artist name",
							"string", artist_convert_str,
							], "log.csv");

					item["name"] = title_convert_str
					item["song_artist_name"] = artist_convert_str
				
				db_obj = None
				exist = False
				if item["type"] == config.ROW_DATA_TYPE_SONG:
					db_obj = sa_db.session.query(Song).filter_by(
						name=item["name"], 
						song_artist_name =item["song_artist_name"], 
						genre_id=item["genre_id"], 
						source_site=item["source_site"],
						artist_page_link=item["artist_link"],
						image_link = item["img_url"]
					).first()

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
						# print "***********************************"
						# print db_obj.name
						# print db_obj.song_artist_name
						# print db_obj.artist_page_link
						# print db_obj.image_link
						# print db_obj.ranking
						# print db_obj.last_ranking
						# print str(item)
						# print "***********************************"
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
					total_count += 1

				except Exception as e:
					sa_db.session.rollback()
					print "?????????????????????????????"
					print item["name"], item["song_artist_name"]
					print url
					print "?????????????????????????????"
					self.show_exception_detail(e)
					break

			except Exception as e:
				self.show_exception_detail(e)

		print "Len=", len(collections),  " Saved=", total_count
		url_item["status"] = "complete"

