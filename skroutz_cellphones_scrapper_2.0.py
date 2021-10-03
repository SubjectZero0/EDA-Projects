# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 13:11:41 2021

@author: iorda
"""

#%%

""" We import these important libraries """

from urllib.request import urlopen as op
from bs4 import BeautifulSoup as Soup
import csv



#%%
""" Create a function that will take a list of urls and the index of the specific url we are about to scrape.

    The goal is to scrape all the urls with one call of this function in a FOR loop """

def page_scraping(my_url_list, url_index):
  
    # Initialize some lists for the columns we want
    prod_name_fu = []
    specs_fu = []
    rating_fu = []
    price_fu = []
    shop_count_fu = []
       
    #we use urlopen (op) to open, read and close the page
    my_client= op(my_url_list[url_index])
        
    page_html = my_client.read()
        
    my_client.close()
    
    #now we use BeautifulSoup to make our soup    
    page_soup = Soup(page_html, 'html.parser')
    
    #By looking at the page html code, we find the main part we need to draw data from, for the cellphones
    cf_cards = page_soup.findAll("li", {"class": ["cf card with-skus-slider", "cf card"]})
     
    # We dive into the specific parts of the html code, to find the data that corresponds to our columns
    # We make a loop that appends the essential data FOR EVERY cellphone listed in the page.    
    for cf_card in cf_cards:
        
        
        prod_name_fu.append(cf_card.div.h2.a["title"])
            
        specs_fu.append(cf_card.div.p["title"])
            
        rating_fu.append(cf_card.div.div.a["title"])
            
        price_class = cf_card.findAll("a", {"class": "js-sku-link sku-link"})
        
        if len(list(price_class[0])) == 2: #noticed an irregularity with the prices in the HTML code. Had to ensure we pick the right value
            price_fu.append(list(price_class[0])[1])
        else:
            price_fu.append(list(price_class[0])[0])  
            
        shop_count_class = cf_card.findAll("span", {"class": "shop-count"})
        
        shop_count_fu.append(shop_count_class[0].text)

    return prod_name_fu, specs_fu, rating_fu, price_fu, shop_count_fu #return all 4 lists
    
    





#%%
""" We set up, by feeding the webpage for cellphones in skroutz and parsing the html
    Currently there are 36 pages. We are going to feed them all to a list
"""
#initialize the list by giving the first page which is different from all the others
my_url = ['https://www.skroutz.gr/c/40/kinhta-thlefwna.html?from=families']

#then, start a counter for the second page
my_url_counter = 2

while len(my_url) < 36:
    
    my_url.append(f"https://www.skroutz.gr/c/40/kinhta-thlefwna.html?from=families&page={my_url_counter}")#make the page be variable inside the url

    my_url_counter = my_url_counter + 1
    
# Now the list is full with all the pages 

#%%
""" This is the main loop. The script uses all the pages and runs the function "page_scraping(my_url_list, url_index)" 
    for all the pages. In the end it fills our columns with the data it has extracted"""

#initialize lists for the columns
prod_name = []
specs = []
rating = []
price = []
shop_count = []

#Run the loop that fills those lists
for i in range(0, len(my_url)):
    
    prod_name_loop, specs_loop, rating_loop, price_loop, shop_count_loop = page_scraping(my_url, i) #all the results from the function go into lists
    
    # The above lists feed our main column lists with every loop 
    prod_name.append(prod_name_loop)
    specs.append(specs_loop)
    rating.append(rating_loop)
    price.append(price_loop)
    shop_count.append(shop_count_loop)
    
#%%
""" Finally we create the csv """

 
filename = 'cellphones_from_skroutz.csv'

with open(filename, 'w', newline = "\n") as f:

    writer = csv.writer(f)
        
    
    for i in range(0, len(prod_name)):    
        
        for j in range(0, len(prod_name[i])):
            
            writer.writerow([prod_name[i][j], specs[i][j], rating[i][j], price[i][j], shop_count[i][j]])
        
    
f.close()        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    