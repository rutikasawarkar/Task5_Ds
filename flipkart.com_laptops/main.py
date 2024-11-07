from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import pandas as pd 

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')

        page.wait_for_load_state('domcontentloaded')
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(200)
        page.screenshot(full_page=True,path='flipkart_laptops.png')

        laptopHtml=page.inner_html('body')
        laptopParse=HTMLParser(laptopHtml)

        laptopContainer= laptopParse.css('div._75nLfW')

        AllLaptops =[]

        for laptop in laptopContainer:
            Title = laptop.css('div.KzDlHZ')[0].text()
            BoldHeading = laptop.css('ul.G4BRas')[0].text()
            Rating = laptop.css('div.XQDdHH')[0].text()
            Price = laptop.css('div.hl05eU')[0].text()
            discount=  laptop.css('div.UkUFwK')[0].text()
            originalPrice =  laptop.css('div.yRaY8j.ZYYwLA')[0].text()
            Imgurl = laptop.css('img.DByuf4')[0].attributes.get('src')
            

            laptop = {
                'Title': 'Title',
                'BoldHeading': 'BoldHeading',
                'rating':'Rating',
                'price':'Price',
                'discount':'discount',
                'originalPrice':'originalPrice',
                'image_Url':'Imgurl'
            }

            AllLaptops.append(laptop)

            print('Title',Title)
            print('BoldHeading',BoldHeading)
            print('Rating',Rating)
            print('price',Price)
            print('discount',discount)
            print('originalPrice',originalPrice)
            print('image_Url',Imgurl)

        laptopData = pd.DataFrame(AllLaptops)
        laptopData.to_csv('laptopData.csv')