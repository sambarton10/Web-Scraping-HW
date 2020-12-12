from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():

    executable_path = {'executable_path' : './/chromedriver'}
    return Browser('chrome', **executable_path, headless = False)
   
def scrape_info():
    browser = init_browser()
    newsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    factsURL = 'https://space-facts.com/mars/'
    hemiURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    featuredimageURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    # Load page into browser
    browser.visit(newsURL)
    # Get Html code as BS object from browser
    newsObj = BeautifulSoup(browser.html, 'html.parser')
    # Find tag for first news headline
    if browser.is_element_present_by_tag('html', wait_time=5):
        firstSlide = newsObj.find('li', class_='slide')
        # Find Title and paragraph of headline
        news_title = firstSlide.find('h3').text
        news_p = firstSlide.find(class_='rollover_description_inner').text
    else:
        print('Page timed out:' + newsURL)
    print(news_title)
    print("------------------------")
    print(news_p)
    
    # Scrape the NASA Featured Image 
    
    # Load page into browser
    browser.visit(featuredimageURL)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    carousel_item = soup.find('article', class_='carousel_item')
    
    style = carousel_item['style']
    
    tempURL = (style.split("'"))
    
    featured_image_url = ('https://www.jpl.nasa.gov/spaceimages/' + tempURL[1])
    print(featured_image_url)
    
    list_of_tables = pd.read_html(factsURL)
    
    mars_dataframe = list_of_tables[0]
    mars_dataframe.to_html()
    
    browser.visit(hemiURL)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    hemisphere_image_urls = []
    
    list_of_results = soup.find_all("h3")
    
    for i in range(len(list_of_results)):
        result_title = list_of_results[i].text
        print(result_title)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
        img_url = soup.find('img', class_='thumb')['src']
        img_url = "https://astrogeology.usgs.gov" + img_url
        print(img_url)
        
        hemis_dict = {"title": result_title, "img_url":img_url}
        hemisphere_image_urls.append(hemis_dict)
        
    print(hemisphere_image_urls)