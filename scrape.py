import urllib.request
from bs4 import BeautifulSoup

sourceUrl = "https://data.gov.uk/dataset/historic-monthly-meteorological-station-data"

# https://stackoverflow.com/a/31857152
# https://stackoverflow.com/a/24226797
def download(url):
	request =  urllib.request.Request(url, data=None, headers={"User-Agent": "Mozilla"})
	response = urllib.request.urlopen(request)
	return response.read().decode("utf-8")

pageHtml = download(sourceUrl)
pageSoup = BeautifulSoup(pageHtml, "html5lib")

links = []

# https://stackoverflow.com/a/5815888
for a in pageSoup.find_all("a", href=True):
	if a["href"].lower().endswith(".txt") and a["href"] not in links:
		links.append(a["href"])

print(f"{len(links)} txt files found. Downloading...")

for link in links:
	fileName = link.split("/")[-1]
	text = download(link)
	with open(f"original_txt/{fileName}", "w", encoding="utf-8") as newFile:
		newFile.write(text)

print("Done.")