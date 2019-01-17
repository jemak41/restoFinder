from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

url = 'https://eatigo.com'
search_items = ['Korean','Indian']

def main():
    getSoup()

def getSoup():
    
    for i in range(len(search_items)):
        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()

        driver.find_element_by_class_name('search--text-field').send_keys(search_items[i])
        time.sleep(1)

        driver.find_element_by_class_name('search--text-field').send_keys(Keys.ENTER)
        time.sleep(1)

        button = driver.find_element_by_xpath("//div[@class='rc-slider-step']/span[5]")
        button.click()

        button = driver.find_element_by_xpath("//div[@class='rc-slider-mark']/span[4]")
        button.click()

        button = driver.find_element_by_xpath("//div[@class='rc-slider-mark']/span[3]")
        button.click()
        time.sleep(1)

        source = driver.page_source
        Soup = BeautifulSoup(source, 'lxml')
        getDetails(Soup)
        driver.close()

def getDetails(soup):
    
    for a in soup.find_all('a', class_='list-card__body'):
        print(a.find('div', class_='list-card__title').text)
        x = a.find('div', class_='list-card__text')
        print(x.text)
        print(x.find_next('div', class_='list-card__text').find_next('div', class_='list-card__text').text)
        print(a.find('span', class_='list-card__rating-text').text + ' Stars')
        for a in soup.find_all('div', class_='discount-item__second'):
            for b in a.find('div'):
                if '5' in b.string:
                    c = b.find_parent('div').find_parent('div').find_previous_sibling('div',
                                                                                      class_='discount-item__first').text
                    print(c)
                    print(b.string)

if __name__ == '__main__':
    main()
