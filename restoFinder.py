from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import nexmo
import restoConfig as rc

url = 'https://eatigo.com'
client = nexmo.Client(key=rc.key, secret=rc.secret)
messages = []
txtCnt = 0
text = ''

def main():
    global search_items
    #search_item = input('Enter keyword: ')
    search_items = rc.search_items

    getSoup()

    y = 0
    charLim = 125
    charLimit = 125
    print(text)
    print(len(text))
    if len(text) > 0:
        txtList = [line.split(',') for line in text]
        txtCnt = int(len(text) / charLim) + 1
        for x in range(txtCnt):
            messages.append('')
            while y < len(txtList):
                messages[x] += txtList[y][0]
                if y == charLimit:
                    charLimit += charLim
                    break
                y += 1

    for a in range(len(messages)):
        #print(str(a + 1) + 'st message: \n' + messages[a] + ' ' + str(len(messages[a])) + 'chars')
        texting(messages[a])



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
    global text

    for a in soup.find_all('a', class_='list-card__body'):
        text += a.find('div', class_='list-card__title').text
        x = a.find('div', class_='list-card__text')
        text += ', ' + x.text
        text += ', @' + x.find_next('div', class_='list-card__text').find_next('div', class_='list-card__text').text
        text += ', ' + a.find('span', class_='list-card__rating-text').text + ' Stars'
        text += '\n'
        for a in soup.find_all('div', class_='discount-item__second'):
            for b in a.find('div'):
                if '5' in b.string:
                    c = b.find_parent('div').find_parent('div').find_previous_sibling('div',
                                                                                      class_='discount-item__first').text
                    text += c + ' '
                    text += b.string + ' '
        text += '\n'
        text += '\n'

def texting(msg):
    client.send_message({
        'from': 'Nexmo',
        'to': rc.number,
        'text': msg,
    })

if __name__ == '__main__':
    main()
