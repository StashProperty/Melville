import requests
from bs4 import BeautifulSoup
import unicodedata


raw = requests.get("https://www.melvillecity.com.au/planning-and-building/development-applications-open-for-public-comment")
soup = BeautifulSoup(raw.content,'html.parser')

raw_rows = soup.find_all("div",{'class':['uk-accordion-content','uk-active']})[1:]

rows = {}
for i in raw_rows:
	if i.find("strong"):
		bold_text = unicodedata.normalize('NFKD',i.find("strong").text).split(" - ")
		council_reference = bold_text[0]
		address = bold_text[1]
		description = unicodedata.normalize('NFKD',i.find_all("p")[1].find(text=True))
		links = i.find_all('a')
		info_link = "https://www.melvillecity.com.au/" + links[0].attrs['href']
		comment_link = links[1].attrs['href']
		rows[council_reference] = [address,description,info_link,comment_link]
