from requests import get
from bs4 import BeautifulSoup
from time import time,sleep
import pandas as pd

requests = 0
steam_tags = {122: 'RPG', 9: 'Strategy', 597: 'Casual', 599: 'Simulation', 1664: 'Puzzle', 21: 'Adventure', 19: 'Action', 701: 'Sports', 492: 'Indie', 4158: "Beat 'em up", 1676: 'RTS', 10437: 'Trivia', 1663: 'FPS', 5055: 'eSports', 1770: 'Board Game', 1773: 'Arcade', 1774: 'Shooter', 3955: 'Character Action Game', 24003: 'Word Game', 4106: 'Action-Adventure', 17389: 'Tabletop', 1741: 'Turn-Based Strategy', 1743: 'Fighting', 1625: 'Platformer', 5379: '2D Platformer', 220585: 'Colony Sim', 1730: 'Sokoban', 198631: 'Mystery Dungeon', 5537: 'Puzzle Platformer', 1698: 'Point & Click', 6506: '3D Fighter', 4328: 'City Builder', 3877: 'Precision Platformer', 1738: 'Hidden Object', 10695: 'Party-Based RPG', 922563: 'Roguevania', 71389: 'Spelling', 9204: 'Immersive Sim', 4434: 'JRPG', 1720: 'Dungeon Crawler', 11014: 'Interactive Fiction', 9271: 'Trading Card Game', 9551: 'Dating Sim', 1670: '4X', 1674: 'Typing', 3978: 'Survival Horror', 1716: 'Roguelike', 1718: 'MOBA', 21725: 'Tactical RPG', 4255: "Shoot 'Em Up", 4777: 'Spectacle fighter', 5900: 'Walking Simulator', 1665: 'Match 3', 1666: 'Card Game', 620519: 'Hero Shooter', 4364: 'Grand Strategy', 42804: 'Action Roguelike', 4486: 'Choose Your Own Adventure', 615955: 'Idler', 353880: 'Looter Shooter', 4885: 'Bullet Hell', 3799: 'Visual Novel', 3959: 'Roguelite', 16598: 'Space Sim', 4231: 'Action RPG', 4474: 'CRPG', 379975: 'Clicker', 791774: 'Card Battler', 1645: 'Tower Defense', 4637: 'Top-Down Shooter', 4758: 'Twin Stick Shooter', 13070: 'Solitaire', 4184: 'Chess', 5395: '3D Platformer', 454187: 'Traditional Roguelike', 1084988: 'Auto Battler', 8666: 'Runner', 4102: 'Combat Racing', 87918: 'Farming Sim', 1752: 'Rhythm', 1754: 'MMORPG', 29482: 'Souls-like', 3813: 'Real Time Tactics', 3814: 'Third-Person Shooter', 56690: 'On-Rails Shooter', 17305: 'Strategy RPG', 1100686: 'Outbreak Sim', 1100687: 'Automobile Sim', 10235: 'Life Sim', 1100688: 'Medical Sim', 1100689: 'Open World Survival Craft', 5300: 'God Game', 176981: 'Battle Royale', 5547: 'Arena Shooter', 4736: '2D Fighter', 1628: 'Metroidvania', 16689: 'Time Management', 26921: 'Political Sim', 4684: 'Wargame', 5652: 'Collectathon', 6621: 'Pinball', 'Id': 'Tag', 1677: 'Turn-Based', 7107: 'Real-Time with Pause', 4161: 'Real-Time', 4325: 'Turn-Based Combat', 6625: 'Time Manipulation', 14139: 'Turn-Based Tactics', 5390: 'Time Attack', 5796: 'Bullet Time', 1734: 'Fast-Paced', 4711: 'Replay Value', 4234: 'Short', 4191: '3D', 4975: '2.5D', 3871: '2D', 1697: 'Third Person', 4791: 'Top-Down', 5851: 'Isometric', 3798: 'Side Scroller', 3839: 'First-Person', 1732: 'Voxel', 4726: 'Cute', 6052: 'Noir', 4145: 'Cinematic', 4305: 'Colorful', 1714: 'Psychedelic', 4094: 'Minimalist', 4252: 'Stylized', 3964: 'Pixel Graphics', 4085: 'Anime', 4004: 'Retro', 4400: 'Abstract', 4195: 'Cartoony', 6815: 'Hand-drawn', 1751: 'Comic Book', 4175: 'Realistic', 31275: 'Text-Based', 4562: 'Cartoon', 12190: 'Boxing', 198913: 'Motorbike', 15868: 'Motocross', 22955: 'Mini Golf', 9564: 'Hunting', 4036: 'Parkour', 7309: 'Skiing', 5914: 'Tennis', 1679: 'Soccer', 13382: 'Archery', 15564: 'Fishing', 47827: 'Wrestling', 699: 'Racing', 96359: 'Skating', 7226: 'Football', 123332: 'Bikes', 1644: 'Driving', 5727: 'Baseball', 28444: 'Snowboarding', 1753: 'Skateboarding', 19568: 'Cycling', 7328: 'Bowling', 6915: 'Martial Arts', 252854: 'BMX', 1746: 'Basketball', 13577: 'Sailing', 324176: 'Hockey', 7038: 'Golf', 1695: 'Open World', 6869: 'Nonlinear', 7250: 'Linear', 3834: 'Exploration', 3810: 'Sandbox', 3878: 'Competitive', 1733: 'Unforgiving', 6730: 'PvE', 4026: 'Difficult', 12057: 'Tutorial', 1775: 'PvP', 1759: 'Perma Death', 4840: '4 Player Local', 1685: 'Co-op', 128: 'Massively Multiplayer', 7368: 'Local Multiplayer', 3841: 'Local Co-Op', 3843: 'Online Co-Op', 5711: 'Team-Based', 4508: 'Co-op Campaign', 17770: 'Asynchronous Multiplayer', 3859: 'Multiplayer', 4182: 'Singleplayer', 4202: 'Trading', 3993: 'Combat', 6971: 'Multiple Endings', 4155: 'Class-Based', 5125: 'Procedural Generation', 5765: 'Gun Customization', 4559: 'Quick-Time Events', 4835: '6DOF', 15172: 'Conversation', 255534: 'Automation', 1717: 'Hex Grid', 15045: 'Flight', 6276: 'Inventory Management', 5981: 'Mining', 5502: 'Hacking', 7926: 'Artificial Intelligence', 1702: 'Crafting', 1669: 'Moddable', 3968: 'Physics', 32322: 'Deckbuilding', 6426: 'Choices Matter', 11104: 'Vehicular Combat', 4994: 'Naval Combat', 1643: 'Building', 1646: 'Hack and Slash', 7332: 'Base Building', 5154: 'Score Attack', 8945: 'Resource Management', 4747: 'Character Customization', 18594: 'FMV', 856791: 'Asymmetric VR', 8253: 'Music-Based Procedural Generation', 5094: 'Narration', 8122: 'Level Editor', 129761: 'ATV', 5923: 'Dark Humor', 1721: 'Psychological Horror', 1710: 'Surreal', 1719: 'Comedy', 5186: 'Psychological', 5984: 'Drama', 4136: 'Funny', 1662: 'Survival', 1667: 'Horror', 19995: 'Dark Comedy', 1654: 'Relaxing', 3835: 'Post-apocalyptic', 4878: 'Parody ', 5608: 'Emotional', 5716: 'Mystery', 4166: 'Atmospheric', 4845: 'Capitalism', 4604: 'Dark Fantasy', 19780: 'Submarine', 4608: 'Swordplay', 1616: 'Trains', 3916: 'Old School', 12472: 'Management', 17927: 'Pool', 6691: "1990's", 4150: 'World War II', 5363: 'Destruction', 51306: 'Foreign', 1680: 'Heist', 7423: 'Sniper', 1681: 'Pirates', 1684: 'Fantasy', 1687: 'Stealth', 3987: 'Historical', 1688: 'Ninja', 13276: 'Tanks', 6041: 'Horses', 5350: 'Family Friendly', 9157: 'Underwater', 5752: 'Robots', 1671: 'Superhero', 1673: 'Aliens', 1036: 'Education', 4821: 'Mechs', 16094: 'Mythology', 1678: 'War', 16250: 'Gambling', 4947: 'Romance', 10397: 'Memes', 10679: 'Time Travel', 9541: 'Demons', 6310: 'Diplomacy', 4376: 'Assassin', 4137: 'Transhumanism', 4018: 'Vampire', 180368: 'Faith', 1708: 'Tactical', 10383: 'Transportation', 17337: 'Lemmings', 7478: 'Illuminati', 5179: 'Cold War', 1651: 'Satire', 6702: 'Mars', 3952: 'Gothic', 5613: 'Detective', 1777: 'Steampunk', 6948: 'Rome', 1659: 'Zombies', 5160: 'Dinosaurs', 6378: 'Crime', 7743: '1980s', 7622: 'Offroad', 4598: 'Alternate History', 4115: 'Cyberpunk', 4236: 'Loot', 9803: 'Snow', 4754: 'Politics', 3942: 'Sci-fi', 13190: 'America', 1647: 'Western', 9592: 'Dynamic Narration', 5030: 'Dystopian ', 31579: 'Otome', 4064: 'Thriller', 4342: 'Dark', 5673: 'Modern', 5794: 'Science', 5432: 'Programming', 10808: 'Supernatural', 6129: 'Logic', 1755: 'Space', 1638: 'Dog', 92092: 'Jet', 21006: 'Underground', 4172: 'Medieval', 5382: 'World War I', 30358: 'Nature', 4295: 'Futuristic', 13906: 'Game Development', 4057: 'Magic', 4695: 'Economy', 6910: 'Naval', 4853: 'Political', 17894: 'Cats', 17015: 'Werewolves', 22602: 'Agriculture', 5372: 'Conspiracy', 44868: 'LGBTQ+', 7432: 'Lovecraftian', 8369: 'Investigation', 4046: 'Dragons', 4168: 'Military', 1694: 'Batman', 1735: 'Star Wars', 1736: 'LEGO', 21722: 'Lara Croft', 12286: 'Warhammer 40K', 5310: 'Games Workshop', 14153: 'Dungeons & Dragons', 7782: 'Cult Classic', 3965: 'Epic', 4190: 'Addictive', 1756: 'Great Soundtrack', 5144: 'Masterpiece', 1693: 'Classic', 5411: 'Beautiful', 493: 'Early Access', 5230: 'Sequel', 7113: 'Crowdfunded', 5153: 'Kickstarter', 5708: 'Remake', 25085: 'Touch-Friendly', 11123: 'Mouse only', 7481: 'Controller', 14906: 'Intentionally Awkward Controls', 27758: 'Voice Control', 7569: 'Grid-Based Movement', 8075: 'TrackIR', 348922: 'Steam Machine', 1445: 'Software Training', 7948: 'Soundtrack', 5407: 'Benchmark', 150626: 'Gaming', 15339: 'Documentary', 776177: '360 Video', 21978: 'VR', 809: 'Photo Editing', 4700: 'Movie', 1038: 'Web Publishing', 3854: 'Lore-Rich', 13782: 'Experimental', 872: 'Animation & Modeling', 113: 'Free to Play', 5348: 'Mod', 1027: 'Audio Production', 15954: 'Silent Protagonist', 603297: 'Hardware', 4242: 'Episodic', 5577: 'RPGMaker', 3796: 'Based On A Novel', 10816: 'Split Screen', 1649: 'GameMaker', 11333: 'Villain Protagonist', 9994: 'Experience', 29363: '3D Vision', 8093: 'Minigames', 8013: 'Software', 7208: 'Female Protagonist', 1742: 'Story Rich', 1621: 'Music', 233824: 'Feature Film', 784: 'Video Production', 84: 'Design & Illustration', 87: 'Utilities', 4667: 'Violent', 5228: 'Blood', 4345: 'Gore', 9130: 'Hentai', 6650: 'Nudity', 12095: 'Sexual Content', 5611: 'Mature', 24904: 'NSFW'}
titles = []
os_lists = []
release_years = []
release_months = []
release_days = []
review_statuss = []
review_percents = []
review_pops = []
price_currs = []
price_origs = []
price_disc_pers = []
game_tagss = []


start_time = time()

#Request url and create bs4 object
url = get("https://store.steampowered.com/search/?sort_by=Released_DESC&os=win&filter=popularnew")
html_soup = BeautifulSoup(url.text, "lxml")

# Obtain whole container of search results
results_div = html_soup.find("div", id = "search_resultsRows")
games = results_div.find_all("a")

# Isolate first game div
game = games[5]

# Title Extraction
game_title = game.span.string
titles.append(game_title)


# Eligible OS Extraction (tuple) (win, mac, lin)
game_os_list = game.find("div", class_ = "col search_name ellipsis").p.find_all("span")

try:
	win = "win"	in game_os_list[0]["class"]
except IndexError:
	win = False
	
try:
	mac = "mac" in game_os_list[1]["class"]
except IndexError:
	mac = False

try:
	linux = "linux" in game_os_list[2]["class"]
except IndexError:
	linux = False

os_list = (win, mac,linux)
os_lists.append(os_list)


# Release Date Extraction
game_release = game.find("div", class_ = "col search_released responsive_secondrow").string

game_release_year = game_release[-4:]
game_release_month = game_release[0:3]
game_release_day = game_release[-8:-6]

release_years.append(game_release_year)
release_months.append(game_release_month)
release_days.append(game_release_day)

# Review Status/Percent/Number of Reviwers (Positive/Mixed/Etc.)
review_status = ""
review_percent = ""
review_pop = ""
switch_one = False
switch_two = False

game_review_container = game.find("div", class_ = "col search_reviewscore responsive_secondrow")
temp = game_review_container.span["data-tooltip-html"].replace("<br>", "_").replace("%", "").replace(",","").replace(" of the ", "-")

for i in range(len(temp)):
	if temp[i] == "_":
		switch_one = True
	elif temp[i] == "-":
		switch_two = True
	elif not switch_one:
		review_status += temp[i]
	elif switch_one and not switch_two:
		review_percent += temp[i]
	elif switch_two and temp[i:i+5] != " user":
		review_pop += temp[i]
	else:
		break

review_percent = int(review_percent)
review_pop = int(review_pop)

review_statuss.append(review_status)
review_percents.append(review_percents)
review_pops.append(review_pop)

# Game Price Extraction
price_curr = ""
price_orig = ""
price_disc_per = ""

#price_list[1]
price_curr_cont = game.find("div", class_ = "col search_price responsive_secondrow")
#price_list[0]
price_disc_per_cont = game.find("div", class_ = "col search_discount responsive_secondrow")

# If there is no sale
if price_disc_per_cont.span == None:
	price_curr = game.find("div", class_ = "col search_price responsive_secondrow").text.replace(" ", "").replace("\n", "").replace("$", "")
	if len(price_curr) == 0:
		price_curr = "N/A"
	else:
		price_curr = price_curr
	price_orig = "N/A"
	price_disc_per = "N/A"
# If there is a sale
else:
	price_curr = game.find("div", class_ = "col search_price discounted responsive_secondrow").text.replace("\n","").replace(" ", "").split("$")[2]
	price_orig = game.find("div", class_ = "col search_price discounted responsive_secondrow").text.replace("\n","").replace(" ", "").split("$")[1]
	price_disc_per = price_disc_per_cont.span.text.replace("-","").replace("%","")

price_currs.append(price_curr)
price_origs.append(price_orig)
price_disc_pers.append(price_disc_per)

# Extracting the tags for the game
tag_keys = games[0]["data-ds-tagids"].replace("]","").replace("[","").split(",")
tag_keys = [int(i) for i in tag_keys]
game_tags = [steam_tags[i] for i in tag_keys]
game_tagss.append(game_tags)


# Adding all parameters into dictionary
game_data = {"Title":titles, 
"OS_List":os_lists, "Release_Month":release_months, "Release_Day":release_days, 
"Release_Year":release_years, "Review_Status":review_statuss, "Review_Percent":review_percents, 
"Review_Pop":review_pops, "Current_Price":price_currs, "Original_Price":price_origs, 
"Discount":price_disc_pers, "Game_Tags":game_tagss}


requests += 1
current_time = time()
elapsed_time = current_time - start_time
print(f"Request: {requests}; Frequency: {1/elapsed_time} requests/s")

game_datas = pd.DataFrame(game_data)
game_datas = game_datas[["Title", "Current_Price", "Original_Price", "Discount", "Review_Status", 
"Review_Percent", "Review_Pop", "Game_Tags", "Release_Day", "Release_Month", "Release_Year"]]
print(game_datas.info())


def main():
	print("hello")



if __name__ == '__main__':
	main()