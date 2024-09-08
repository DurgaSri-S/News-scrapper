"""    
  This program scraps the news headlines from websites
"""
import requests as req
from bs4 import BeautifulSoup as bs
import sys


def indian_express_news(source, topic):
    """
    Extract the exact news headlines respect to the user selected topic
    :param source: Parsed web page source
    :param topic: User selected topic
    :return: list of news headlines
    """
    news_headlines = []
    if topic == "tech":
        h3_tags = source.find_all('h3', class_="")
        for h3_tag in h3_tags:
            news_headlines.append(h3_tag.find('a').get_text())
    else:
        h2_tags = source.find_all('h2', class_="title")
        for h2_tag in h2_tags:
            news_headlines.append(h2_tag.find('a').get_text())
    return news_headlines


def hindustan_times_news(source, topic):
    """
    Extract the exact news headlines respect to the user selected topic
    :param source: Parsed web page source
    :param topic: User selected topic
    :return: list of news headlines
    """

    news_headlines = []
    h3_tags = source.find_all('h3', class_="hdg3")
    for h3_tag in h3_tags:
        news_headlines.append(h3_tag.find('a').get_text())
    return news_headlines

DEFAULT_LIMIT = 10
base_url_express = "https://indianexpress.com/"
base_url_times = "https://www.hindustantimes.com/"

# Get topic from user
print("""
1. tech
2. sports
3. education
4. lifestyle
5. business
""")
topic = input("Choose one topic : ").lower()

if topic == "tech":
    express_url = base_url_express + "section/technology/"
    times_url = base_url_times + "technology"
elif topic == "sports":
    express_url = base_url_express + "section/sports/"
    times_url = base_url_times + "sports"
elif topic == "education":
    express_url = base_url_express + "section/education/"
    times_url = base_url_times + "education"
elif topic == "lifestyle":
    express_url = base_url_express + "section/lifestyle/"
    times_url = base_url_times + "lifestyle"
elif topic == "business":
    express_url = base_url_express + "section/business/"
    times_url = base_url_times + "business"
else:
    print("Invalid input")
    sys.exit(1)

base_formatted_url = [express_url, times_url]
try:
    news_list = []
    # If this missed, some sites may throw access denied error
    header = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in base_formatted_url:
        # Get response from server by giving URL
        response = req.get(url, headers=header)
        # Choose html parser to parse the response
        page = bs(response.text, 'html.parser')
        # Calling necessary function
        if "indian" in url:
            news_list.extend(indian_express_news(page, topic))
        else:
            news_list.extend(hindustan_times_news(page, topic))

    print("Total news entries fetched : ", len(news_list))

    for index, news in enumerate(news_list, start= 1):
        print(str(index).zfill(2) + ". " + news)
        if index == DEFAULT_LIMIT:
            break

except Exception as e:
    print("Some exception occurred", e)
