import requests
import bs4
from datetime import date
import schedule
import time
import random


html_soup = bs4.BeautifulSoup(requests.get("https://www.walmart.com/ip/Apple-AirPods-Pro/520468661").text, "lxml")

b = []

def get_price() -> None:



	price_cont = html_soup.find("div", class_ = "prod-PriceHero")

	date_entry = str(date.today())
	price = float(price_cont.span.span.span.span.text[1:])

	price_date_tuple = (date_entry,price)

	b.append(price_date_tuple)




	print(b)

def main():

	

	schedule.every().day.at("10:00").do(get_price)

	while True:

		schedule.run_pending()
		time.sleep(1)



if __name__ == "__main__":
	main()