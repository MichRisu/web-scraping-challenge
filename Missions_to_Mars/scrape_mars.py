from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # ----- Visit Mars news site ----- #
    mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_url)

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

    # ----- Visit JPL site ----- #
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    # Scrape page into soup
    jpl_html = browser.html
    soup = bs(jpl_html, 'html.parser')

    # Find the featured image from home page and click Full Image button
    browser.links.find_by_partial_text('FULL IMAGE')
    time.sleep(1)

    # Find the more info button and click
    browser.links.find_by_partial_text('more info')

    # Use BeautifulSoup to find the full size .jpg image URL
    jpl_image = soup.find('figure', class_='lede').find('a')['href']
    jpl_base = 'https://www.jpl.nasa.gov'

    featured_image_url = jpl_base + jpl_image

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
    df_mars.to_html('Mars_Facts_table.html')

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

    # Quit the browser after scraping
    browser.quit()

    # Return results
    return mars_data        