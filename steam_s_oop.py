import bs4
import requests
import time
import random
import pandas

class contExtractor():
	'''
	This class is used to extract containers from a url through the bs4 and requests packages
	'''
	def __init__(self, url: str):
		self.results_cont = bs4.BeautifulSoup(requests.get(url).text, features = "lxml").find("div", id = "search_resultsRows")
		self.game_conts = self.results_cont.find_all("a")

	# Returns entire container for game that is within the search results
	def GetGameCont(self, game_num: int):
		return self.game_conts[game_num]

	# Returns the container that contains the title, and eligible OS's
	def GetMainCont(self, game_num: int):
		return self.game_conts[game_num].find("div", class_ = "col search_name ellipsis")

	# Returns the container containing the date
	def GetDateCont(self, game_num: int):
		return self.game_conts[game_num].find("div", class_ = "col search_released responsive_secondrow")

	# Returns the container containing the review status, percentage, and number of reviewers
	def GetRateCont(self, game_num: int):
		return self.game_conts[game_num].find("div", class_ = "col search_reviewscore responsive_secondrow")

	# Returns the container containing price information
	def GetPriceCont(self, game_num: int):
		return self.game_conts[game_num].find("div", class_ = "col search_price_discount_combined responsive_secondrow")


# Now the functions for extracting all the information will begin below


# Gets title of game
def get_title(obj: contExtractor, num: int) -> str:
	assert type(obj) == contExtractor
	assert num >= 0, "number must be an integer that is at least 0"

	return obj.GetMainCont(num).span.string

# Returns tuple of booleans corresponding to eligible os's (win,mac,linux)
def get_oss(obj: contExtractor, num: int) -> tuple:
	assert type(obj) == contExtractor
	assert num >= 0, "number must be an integer that is at least 0"

	ls = obj.GetMainCont(num).p.find_all("span")

	try:
		win = "win"	in ls[0]["class"]
	except IndexError:
		win = False
	
	try:
		mac = "mac" in ls[1]["class"]
	except IndexError:
		mac = False

	try:
		linux = "linux" in ls[2]["class"]
	except IndexError:
		linux = False

	return (win, mac,linux)

# Returns list of release date info as [month, day, year] for game indexed num in the search results
def get_release_info(obj: contExtractor, num: int) -> list:
	assert type(obj) == contExtractor
	assert num >= 0, "number must be an integer that is at least 0"

	year = obj.GetDateCont(num).string[-4:]
	month = obj.GetDateCont(num).string[0:3]
	day = obj.GetDateCont(num).string[-8:-6]

	return [month, day, year]


# Returns list of review info as [review_status, % positive reviews, # of reviewers]
def get_review_info(obj: contExtractor, num: int) -> list:
	assert type(obj) == contExtractor
	assert num >= 0, "number must be an integer that is at least 0"

	status = ""
	percent = ""
	pop = ""
	switch_one = False
	switch_two = False

	try:
		temp = obj.GetRateCont(num).span["data-tooltip-html"].replace("<br>", "_").replace("%", "").replace(",","").replace(" of the ", "-")
		for i in range(len(temp)):
			if temp[i] == "_":
				switch_one = True
			elif temp[i] == "-":
				switch_two = True
			elif not switch_one:
				status += temp[i]
			elif switch_one and not switch_two:
				percent += temp[i]
			elif switch_two and temp[i:i+5] != " user":
				pop += temp[i]
			else:
				break
		return [status, int(percent), int(pop)]
	except TypeError:
		status = "N/A"
		percent = "N/A"
		pop = "N/A"
		return [status, percent, pop]

	
                                                  									  


# Returns list of price info as [current_price, original_price, discount_percentage]
def get_price_info(obj: contExtractor, num: int) -> list:
	assert type(obj) == contExtractor
	assert num >= 0, "number must be an integer that is at least 0"

	curr = ""
	orig = ""
	disc_per = ""

	# List of price info as [discount_div, price_div]
	price_list = obj.GetPriceCont(num).find_all("div")

	# If there is no sale
	if price_list[0].span == None:
		curr = price_list[1].text.replace(" ", "").replace("\n", "").replace("$", "").replace("\r","")
		if len(curr) == 0:
			curr = "N/A"
		orig = "N/A"
		disc_per = "N/A"
	# If there is a sale
	else:
		curr = price_list[1].text.strip().split("$")[2]
		orig = price_list[1].text.strip().split("$")[1]
		disc_per = price_list[0].span.text

	return [curr, orig, disc_per]

# Returns a list of tags associated to the game
def get_tag_info(obj: contExtractor, num: int) -> list:
	assert type(obj) == contExtractor
	assert num >= 0, "number must be an integer that is at least 0"

	steam_tags = {122: 'RPG', 9: 'Strategy', 597: 'Casual', 599: 'Simulation', 1664: 'Puzzle', 21: 'Adventure', 19: 'Action', 701: 'Sports', 492: 'Indie', 4158: "Beat 'em up", 1676: 'RTS', 10437: 'Trivia', 1663: 'FPS', 5055: 'eSports', 1770: 'Board Game', 1773: 'Arcade', 1774: 'Shooter', 3955: 'Character Action Game', 24003: 'Word Game', 4106: 'Action-Adventure', 17389: 'Tabletop', 1741: 'Turn-Based Strategy', 1743: 'Fighting', 1625: 'Platformer', 5379: '2D Platformer', 220585: 'Colony Sim', 1730: 'Sokoban', 198631: 'Mystery Dungeon', 5537: 'Puzzle Platformer', 1698: 'Point & Click', 6506: '3D Fighter', 4328: 'City Builder', 3877: 'Precision Platformer', 1738: 'Hidden Object', 10695: 'Party-Based RPG', 922563: 'Roguevania', 71389: 'Spelling', 9204: 'Immersive Sim', 4434: 'JRPG', 1720: 'Dungeon Crawler', 11014: 'Interactive Fiction', 9271: 'Trading Card Game', 9551: 'Dating Sim', 1670: '4X', 1674: 'Typing', 3978: 'Survival Horror', 1716: 'Roguelike', 1718: 'MOBA', 21725: 'Tactical RPG', 4255: "Shoot 'Em Up", 4777: 'Spectacle fighter', 5900: 'Walking Simulator', 1665: 'Match 3', 1666: 'Card Game', 620519: 'Hero Shooter', 4364: 'Grand Strategy', 42804: 'Action Roguelike', 4486: 'Choose Your Own Adventure', 615955: 'Idler', 353880: 'Looter Shooter', 4885: 'Bullet Hell', 3799: 'Visual Novel', 3959: 'Roguelite', 16598: 'Space Sim', 4231: 'Action RPG', 4474: 'CRPG', 379975: 'Clicker', 791774: 'Card Battler', 1645: 'Tower Defense', 4637: 'Top-Down Shooter', 4758: 'Twin Stick Shooter', 13070: 'Solitaire', 4184: 'Chess', 5395: '3D Platformer', 454187: 'Traditional Roguelike', 1084988: 'Auto Battler', 8666: 'Runner', 4102: 'Combat Racing', 87918: 'Farming Sim', 1752: 'Rhythm', 1754: 'MMORPG', 29482: 'Souls-like', 3813: 'Real Time Tactics', 3814: 'Third-Person Shooter', 56690: 'On-Rails Shooter', 17305: 'Strategy RPG', 1100686: 'Outbreak Sim', 1100687: 'Automobile Sim', 10235: 'Life Sim', 1100688: 'Medical Sim', 1100689: 'Open World Survival Craft', 5300: 'God Game', 176981: 'Battle Royale', 5547: 'Arena Shooter', 4736: '2D Fighter', 1628: 'Metroidvania', 16689: 'Time Management', 26921: 'Political Sim', 4684: 'Wargame', 5652: 'Collectathon', 6621: 'Pinball', 'Id': 'Tag', 1677: 'Turn-Based', 7107: 'Real-Time with Pause', 4161: 'Real-Time', 4325: 'Turn-Based Combat', 6625: 'Time Manipulation', 14139: 'Turn-Based Tactics', 5390: 'Time Attack', 5796: 'Bullet Time', 1734: 'Fast-Paced', 4711: 'Replay Value', 4234: 'Short', 4191: '3D', 4975: '2.5D', 3871: '2D', 1697: 'Third Person', 4791: 'Top-Down', 5851: 'Isometric', 3798: 'Side Scroller', 3839: 'First-Person', 1732: 'Voxel', 4726: 'Cute', 6052: 'Noir', 4145: 'Cinematic', 4305: 'Colorful', 1714: 'Psychedelic', 4094: 'Minimalist', 4252: 'Stylized', 3964: 'Pixel Graphics', 4085: 'Anime', 4004: 'Retro', 4400: 'Abstract', 4195: 'Cartoony', 6815: 'Hand-drawn', 1751: 'Comic Book', 4175: 'Realistic', 31275: 'Text-Based', 4562: 'Cartoon', 12190: 'Boxing', 198913: 'Motorbike', 15868: 'Motocross', 22955: 'Mini Golf', 9564: 'Hunting', 4036: 'Parkour', 7309: 'Skiing', 5914: 'Tennis', 1679: 'Soccer', 13382: 'Archery', 15564: 'Fishing', 47827: 'Wrestling', 699: 'Racing', 96359: 'Skating', 7226: 'Football', 123332: 'Bikes', 1644: 'Driving', 5727: 'Baseball', 28444: 'Snowboarding', 1753: 'Skateboarding', 19568: 'Cycling', 7328: 'Bowling', 6915: 'Martial Arts', 252854: 'BMX', 1746: 'Basketball', 13577: 'Sailing', 324176: 'Hockey', 7038: 'Golf', 1695: 'Open World', 6869: 'Nonlinear', 7250: 'Linear', 3834: 'Exploration', 3810: 'Sandbox', 3878: 'Competitive', 1733: 'Unforgiving', 6730: 'PvE', 4026: 'Difficult', 12057: 'Tutorial', 1775: 'PvP', 1759: 'Perma Death', 4840: '4 Player Local', 1685: 'Co-op', 128: 'Massively Multiplayer', 7368: 'Local Multiplayer', 3841: 'Local Co-Op', 3843: 'Online Co-Op', 5711: 'Team-Based', 4508: 'Co-op Campaign', 17770: 'Asynchronous Multiplayer', 3859: 'Multiplayer', 4182: 'Singleplayer', 4202: 'Trading', 3993: 'Combat', 6971: 'Multiple Endings', 4155: 'Class-Based', 5125: 'Procedural Generation', 5765: 'Gun Customization', 4559: 'Quick-Time Events', 4835: '6DOF', 15172: 'Conversation', 255534: 'Automation', 1717: 'Hex Grid', 15045: 'Flight', 6276: 'Inventory Management', 5981: 'Mining', 5502: 'Hacking', 7926: 'Artificial Intelligence', 1702: 'Crafting', 1669: 'Moddable', 3968: 'Physics', 32322: 'Deckbuilding', 6426: 'Choices Matter', 11104: 'Vehicular Combat', 4994: 'Naval Combat', 1643: 'Building', 1646: 'Hack and Slash', 7332: 'Base Building', 5154: 'Score Attack', 8945: 'Resource Management', 4747: 'Character Customization', 18594: 'FMV', 856791: 'Asymmetric VR', 8253: 'Music-Based Procedural Generation', 5094: 'Narration', 8122: 'Level Editor', 129761: 'ATV', 5923: 'Dark Humor', 1721: 'Psychological Horror', 1710: 'Surreal', 1719: 'Comedy', 5186: 'Psychological', 5984: 'Drama', 4136: 'Funny', 1662: 'Survival', 1667: 'Horror', 19995: 'Dark Comedy', 1654: 'Relaxing', 3835: 'Post-apocalyptic', 4878: 'Parody ', 5608: 'Emotional', 5716: 'Mystery', 4166: 'Atmospheric', 4845: 'Capitalism', 4604: 'Dark Fantasy', 19780: 'Submarine', 4608: 'Swordplay', 1616: 'Trains', 3916: 'Old School', 12472: 'Management', 17927: 'Pool', 6691: "1990's", 4150: 'World War II', 5363: 'Destruction', 51306: 'Foreign', 1680: 'Heist', 7423: 'Sniper', 1681: 'Pirates', 1684: 'Fantasy', 1687: 'Stealth', 3987: 'Historical', 1688: 'Ninja', 13276: 'Tanks', 6041: 'Horses', 5350: 'Family Friendly', 9157: 'Underwater', 5752: 'Robots', 1671: 'Superhero', 1673: 'Aliens', 1036: 'Education', 4821: 'Mechs', 16094: 'Mythology', 1678: 'War', 16250: 'Gambling', 4947: 'Romance', 10397: 'Memes', 10679: 'Time Travel', 9541: 'Demons', 6310: 'Diplomacy', 4376: 'Assassin', 4137: 'Transhumanism', 4018: 'Vampire', 180368: 'Faith', 1708: 'Tactical', 10383: 'Transportation', 17337: 'Lemmings', 7478: 'Illuminati', 5179: 'Cold War', 1651: 'Satire', 6702: 'Mars', 3952: 'Gothic', 5613: 'Detective', 1777: 'Steampunk', 6948: 'Rome', 1659: 'Zombies', 5160: 'Dinosaurs', 6378: 'Crime', 7743: '1980s', 7622: 'Offroad', 4598: 'Alternate History', 4115: 'Cyberpunk', 4236: 'Loot', 9803: 'Snow', 4754: 'Politics', 3942: 'Sci-fi', 13190: 'America', 1647: 'Western', 9592: 'Dynamic Narration', 5030: 'Dystopian ', 31579: 'Otome', 4064: 'Thriller', 4342: 'Dark', 5673: 'Modern', 5794: 'Science', 5432: 'Programming', 10808: 'Supernatural', 6129: 'Logic', 1755: 'Space', 1638: 'Dog', 92092: 'Jet', 21006: 'Underground', 4172: 'Medieval', 5382: 'World War I', 30358: 'Nature', 4295: 'Futuristic', 13906: 'Game Development', 4057: 'Magic', 4695: 'Economy', 6910: 'Naval', 4853: 'Political', 17894: 'Cats', 17015: 'Werewolves', 22602: 'Agriculture', 5372: 'Conspiracy', 44868: 'LGBTQ+', 7432: 'Lovecraftian', 8369: 'Investigation', 4046: 'Dragons', 4168: 'Military', 1694: 'Batman', 1735: 'Star Wars', 1736: 'LEGO', 21722: 'Lara Croft', 12286: 'Warhammer 40K', 5310: 'Games Workshop', 14153: 'Dungeons & Dragons', 7782: 'Cult Classic', 3965: 'Epic', 4190: 'Addictive', 1756: 'Great Soundtrack', 5144: 'Masterpiece', 1693: 'Classic', 5411: 'Beautiful', 493: 'Early Access', 5230: 'Sequel', 7113: 'Crowdfunded', 5153: 'Kickstarter', 5708: 'Remake', 25085: 'Touch-Friendly', 11123: 'Mouse only', 7481: 'Controller', 14906: 'Intentionally Awkward Controls', 27758: 'Voice Control', 7569: 'Grid-Based Movement', 8075: 'TrackIR', 348922: 'Steam Machine', 1445: 'Software Training', 7948: 'Soundtrack', 5407: 'Benchmark', 150626: 'Gaming', 15339: 'Documentary', 776177: '360 Video', 21978: 'VR', 809: 'Photo Editing', 4700: 'Movie', 1038: 'Web Publishing', 3854: 'Lore-Rich', 13782: 'Experimental', 872: 'Animation & Modeling', 113: 'Free to Play', 5348: 'Mod', 1027: 'Audio Production', 15954: 'Silent Protagonist', 603297: 'Hardware', 4242: 'Episodic', 5577: 'RPGMaker', 3796: 'Based On A Novel', 10816: 'Split Screen', 1649: 'GameMaker', 11333: 'Villain Protagonist', 9994: 'Experience', 29363: '3D Vision', 8093: 'Minigames', 8013: 'Software', 7208: 'Female Protagonist', 1742: 'Story Rich', 1621: 'Music', 233824: 'Feature Film', 784: 'Video Production', 84: 'Design & Illustration', 87: 'Utilities', 4667: 'Violent', 5228: 'Blood', 4345: 'Gore', 9130: 'Hentai', 6650: 'Nudity', 12095: 'Sexual Content', 5611: 'Mature', 24904: 'NSFW'}
	
	try:
		tag_keys = obj.GetGameCont(num)["data-ds-tagids"].replace("]","").replace("[","").split(",")
		tag_keys = [int(i) for i in tag_keys]

		game_tags = []

		for i in range(len(tag_keys)):
			try:
				game_tags.append(steam_tags[tag_keys[i]])
			except KeyError:
				game_tags.append(tag_keys[i])
	except KeyError:
		game_tags = []

	return game_tags


''' 
	Now that all the functions for the single game have been made,
	functions for the iteration over the search results and 
	consequential collection of each parameter into lists will be 
	made below
'''

def get_title_list(obj: contExtractor) -> list:
	return [get_title(e,i) for i in range(len(obj.game_conts))]

def get_oss_list(obj: contExtractor) -> list:
	return [get_oss(e,i) for i in range(len(obj.game_conts))]	

def get_release_month_list(obj: contExtractor) -> list:
	return [get_release_info(e,i)[0] for i in range(len(obj.game_conts))]

def get_release_day_list(obj: contExtractor) -> list:
	return [get_release_info(e,i)[1] for i in range(len(obj.game_conts))]

def get_release_year_list(obj: contExtractor) -> list:
	return [get_release_info(e,i)[2] for i in range(len(obj.game_conts))]

def get_review_status_list(obj: contExtractor) -> list:
	return [get_review_info(e,i)[0] for i in range(len(obj.game_conts))]

def get_review_per_list(obj: contExtractor) -> list:
	return [get_review_info(e,i)[1] for i in range(len(obj.game_conts))]

def get_review_pop_list(obj: contExtractor) -> list:
	return [get_review_info(e,i)[2] for i in range(len(obj.game_conts))]

def get_price_curr_list(obj: contExtractor) -> list:
	return [get_price_info(e,i)[0] for i in range(len(obj.game_conts))]

def get_price_orig_list(obj: contExtractor) -> list:
	return [get_price_info(e,i)[1] for i in range(len(obj.game_conts))]	

def get_price_disc_list(obj: contExtractor) -> list:
	return [get_price_info(e,i)[2] for i in range(len(obj.game_conts))]		

def get_tag_info_list(obj: contExtractor) -> list:
	return [get_tag_info(e,i) for i in range(len(obj.game_conts))]

def get_info_dict(obj: contExtractor) -> dict:
	'''
	Compiles all parameters of games in the whole page into a dictionary
	'''
	info_dict = {"Title":get_title_list(obj), 
	"Available_OS":get_oss_list(obj),
	"Month":get_release_month_list(obj), 
	"Day":get_release_day_list(obj),
	"Year":get_release_year_list(obj), 
	"Current_Price":get_price_curr_list(obj),
	"Original_Price":get_price_orig_list(obj),
	"Discount_Percentage":get_price_disc_list(obj),
	"Review_Status":get_review_status_list(obj),
	"Percentage_Positive_Reviews":get_review_per_list(obj),
	"Reviewer_Count":get_review_pop_list(obj),
	"Game_Tags":get_tag_info_list(obj)  
	}

	return info_dict

def get_data() -> dict:
	request_count = 0
	data = {}
	titles = []
	os_list = []
	months = []
	days = []
	years = []
	price_curr_list = []
	price_orig_list = []
	price_disc_list = []
	review_status_list = []
	review_per_list = []
	review_pop_list = []
	tag_list = []

	urls = ["https://store.steampowered.com/search/?sort_by=Released_DESC&os=win&filter=popularnew" + "&page=" + str(i) for i in range(1,11)]
	for url in urls:
		
		start = time.time()
		obj = contExtractor(url)
		request_count += 1
		
		for i in range(len(obj.game_conts)):
			data.update({"Title":get_title(obj,i), 
			"Available_OS":get_oss(obj,i),
			"Month":get_release_info(obj,i)[0], 
			"Day":get_release_info(obj,i)[1],
			"Year":get_release_info(obj,i)[2], 
			"Current_Price":get_price_info(obj,i)[0],
			"Original_Price":get_price_info(obj,i)[1],
			"Discount_Percentage":get_price_info(obj,i)[2],
			"Review_Status":get_review_info(obj,i)[0],
			"Percentage_Positive_Reviews":get_review_info(obj,i)[1],
			"Reviewer_Count":get_review_info(obj,i)[2],
			"Game_Tags":get_tag_info(obj,i)})
		
		print(data)
		time.sleep(random.randint(3,5))
		end = time.time()
		elapsed = end - start
		print(f"Request: {request_count}; Frequency: {1/elapsed} requests/s")

		# print(pandas.DataFrame(data).info())
	return data

# Initialization of contExtractor object
e = contExtractor("https://store.steampowered.com/search/?sort_by=Released_DESC&os=win&filter=popularnew")


def main():

	# data = get_data()
	# data = pandas.DataFrame(data)
	# print("\n")
	# print(data.info())
	for i in range(len(e.game_conts)):
		try:
			get_tag_info(e,i)
		except KeyError:
			print(i, get_title(e,i))


if __name__ == "__main__":
	main()