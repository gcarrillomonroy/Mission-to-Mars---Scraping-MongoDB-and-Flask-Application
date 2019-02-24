from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    ### NASA Mars News ###
    # Visit visitcostarica.herokuapp.com
    url = 'https://mars.nasa.gov/news/'    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find('div', class_='content_title').text.strip()
    news_p     = soup.find('div', class_='rollover_description_inner').text.strip()



    ### JPL Mars Space Images - Featured Image ###
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    img = soup.find('article', class_='carousel_item')
    featured_image_url = 'https://www.jpl.nasa.gov' + img['style'][23:75]

    browser.quit()

    ### Mars Facts ###
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    dict_table = df.to_dict('list')
    dict_table = {str(key): value for key, value in  dict_table.items()}
    #df.columns = ['Fact', 'Value']



    ### Mars Hemispheres ###
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []
    dict = {}
    url = 'https://astrogeology.usgs.gov'

    img = soup.find_all('a', class_='itemLink product-item')
    for i in img:
        if(i.get_text() != ''):
            #dict = {'title': i.get_text(),
            #        'img_url' : url + i['href']}
            #hemisphere_image_urls.append(dict)                
            
            browser.visit(url + i['href'])    
            
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            
            tmp = soup.find('div', class_='downloads').find('a')['href']
            dict = {'title': i.get_text(),
                    'img_url' : tmp} 
            hemisphere_image_urls.append(dict)        
            browser.back()  

    browser.quit()

    print(dict_table)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "table" : dict_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }

    # Return results
    return mars_data
