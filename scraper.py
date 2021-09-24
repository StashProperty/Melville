import requests
from bs4 import BeautifulSoup
import unicodedata
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd


URL = "https://www.melvillecity.com.au/planning-and-building/development-applications-open-for-public-comment"
DATABASE = "data.sqlite"
DATA_TABLE = "data"
PROCESSED_FILES_TABLE = "files_processed"
PROCESSED_FILES_COLUMN = "name"

engine = create_engine(f'sqlite:///{DATABASE}', echo=False)
pd.DataFrame(columns=[PROCESSED_FILES_COLUMN]).to_sql(PROCESSED_FILES_TABLE, con=engine, if_exists="append")




raw = requests.get(URL)
soup = BeautifulSoup(raw.content,'html.parser')

raw_rows = soup.find_all("div",{'class':['uk-accordion-content','uk-active']})[1:]

rows = pd.DataFrame(columns=['council_reference','address','description','date_scraped','info_url','comment_url'])
date = datetime.strftime(datetime.now(),'%d-%m-%Y')
counter = 0
for i in raw_rows:
	if i.find("strong"):
		bold_text = unicodedata.normalize('NFKD',i.find("strong").text).split(" - ")
		council_reference = bold_text[0]
		address = bold_text[1]
		description = unicodedata.normalize('NFKD',i.find_all("p")[1].find(text=True))
		links = i.find_all('a')
		info_link = "https://www.melvillecity.com.au/" + links[0].attrs['href']
		comment_link = links[1].attrs['href']
		rows.loc[counter] = [council_reference, address,description,date,info_link,comment_link]
		counter += 1
rows.to_sql(DATA_TABLE,con=engine,if_exists='append',index=False)

