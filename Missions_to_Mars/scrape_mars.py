from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # ----- Visit Mars news site ----- #
    mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_url)
    time.sleep(3)

    #Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find the current news titles 
    titles = soup.find_all('div', class_="content_title")

    # Find the news paragraphs
    paras = soup.find_all('div', class_="article_teaser_body")

    # Assign the text to variables with text only
    news_title = titles[1].text
    news_p = paras[1].text
    time.sleep(5)

    # ----- Visit JPL site ----- #
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(3)

    # Create BeautifulSoup object
    jpl_html = browser.html
    soup = bs(jpl_html, 'html.parser')

    # Find the url for the featured image
    jpl_image_path = soup.find('a', class_='button fancybox')['data-fancybox-href']

    jpl_base = 'https://www.jpl.nasa.gov'
    featured_image_url = jpl_base + jpl_image_path
    time.sleep(3)
    
    # ----- Visit site for Mars facts ----- #
    # Use Pandas to scrape the table of facts
    facts_url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(facts_url)
    mars_table

    # Organize table by setting columns and index
    df_mars = mars_table[0]
    df_mars.columns = ['Description', 'Value']
    df_mars.set_index('Description', inplace=True)
    df_mars.head()

    # Use Pandas to convert the data to a HTML table string
    mars_facts_table = df_mars.to_html()

    # ----- Visit USGS Astrogeology site ----- #
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)

    # Scrape page into soup
    hemis_html = browser.html
    soup = bs(hemis_html, 'html.parser')

    # Find title and full image url for each hemisphere and return to a dictionary
    hemis_base_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = []

    results = soup.find_all('div', class_='item')
    for result in results:
        title = result.find('h3').text
  
        thumb_url = hemis_base_url + result.find('a')['href']
 
        response = requests.get(thumb_url)
        soup = bs(response.text, 'html.parser')
        
        img_url = soup.find('ul').li.a['href']
        
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    # Store data in a dictionary
    mars_data = {
    "news_title": news_title,
    "news_paragraph": news_p,
    "featured_image": featured_image_url,
    "mars_facts": mars_facts_table, 
    "hemispheres": hemisphere_image_urls
    }

    # Quit the browser after scraping
    browser.quit()

    # Return results
    return mars_data        