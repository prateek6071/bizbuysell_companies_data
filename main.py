from selenium import webdriver
from time import sleep
import pandas as pd
from webdrivermanager.chrome import ChromeDriverManager


driver = webdriver.Chrome(executable_path=r'D:\chromedriver.exe')
driver.get('https://www.bizbuysell.com/users/login.aspx?returnurl=/mybbs')
username=driver.find_element_by_id('ctl00_ctl00_Content_ContentPlaceHolder1_LoginControl_txtUserName')
username.send_keys('prateek@fmail.com')
password=driver.find_element_by_id('ctl00_ctl00_Content_ContentPlaceHolder1_LoginControl_txtPassword')
password.send_keys('123456')
submit_login=driver.find_element_by_id('ctl00_ctl00_Content_ContentPlaceHolder1_LoginControl_BtnLogin')
submit_login.click()
driver.implicitly_wait(2)
driver.get('http://bizbuysell.com')
driver.implicitly_wait(3)
location='california'
business_type='manufacturing'
driver.get('https://www.bizbuysell.com/'+location+'/'+ business_type+'-businesses-for-sale?q=bHQ9MzAsNDAsODA%3D')
driver.implicitly_wait(3)
diamond=0
showcase=0
broker=0
container=[]
while(diamond+showcase+broker!=43):
    diamond_path='//*[@id="search-results"]/app-bfs-listing-container/div/app-listing-diamond['+str(diamond+1)+']'
    showcase_path='//*[@id="search-results"]/app-bfs-listing-container/div/app-listing-showcase['+str(showcase+1)+']'
    broker_path='//*[@id="search-results"]/app-bfs-listing-container/div/app-listing-inline-broker['+str(broker+1)+']'
    path = driver.find_element_by_xpath(showcase_path)

    try:
        title = path.find_element_by_class_name('title.ng-star-inserted')
        info = title.text
        href = path.find_element_by_tag_name('a').get_attribute('href')
        id = path.find_element_by_tag_name('a').get_attribute('id')

        location = path.find_element_by_class_name('location.ng-star-inserted')
        location=location.text
        description = path.find_element_by_class_name('description.ng-star-inserted')
        description=description.text
        fin = []
        try:
            price = path.find_element_by_class_name('col-2.tablet-col-1.hide-on-mobile.finance')
            fin = price.text.split()
            asking_price = fin[0]
            print(asking_price)
        except:
            asking_price="private"
            print(asking_price)

        try:
            driver.get(href)
            driver.implicitly_wait(3)
            seller = []
            sellername = driver.find_element_by_class_name('broker')
            seller = sellername.text.split()
            seller_name = seller[3] + ' ' + seller[4]
        except:
            seller_name = "private"

        try:
            idnew = driver.find_element_by_id(id)
            idnew = idnew.get_attribute('href')
            phone = idnew.split(':')
            phone_number = phone[1]
            print(phone_number)
            showcase = showcase + 1
            driver.get('https://www.bizbuysell.com/california/manufacturing-businesses-for-sale?q=bHQ9MzAsNDAsODA%3D')
        except:
            try:
                idnew = driver.find_element_by_xpath('//*[@id="lblViewTpnTelephone_' + id + '"]/a').get_attribute('href')
                idnew = id.split(':')[1]
                phone_number=idnew
                print(phone_number)
                showcase = showcase + 1
                driver.get(
                    'https://www.bizbuysell.com/california/manufacturing-businesses-for-sale?q=bHQ9MzAsNDAsODA%3D')
            except:
                phone_number = "private"
                print(phone_number)
                showcase = showcase + 1
                driver.get(
                    'https://www.bizbuysell.com/california/manufacturing-businesses-for-sale?q=bHQ9MzAsNDAsODA%3D')
    except:
        showcase=showcase+1
        driver.get('https://www.bizbuysell.com/california/manufacturing-businesses-for-sale?q=bHQ9MzAsNDAsODA%3D')
    container.append({'company_name':info,'company_url':href,'description':description,'location':location,'id':id,'seller_name':seller_name,'phone_number':phone_number})
    driver.implicitly_wait(3)

df=pd.DataFrame(container)
df.to_excel('bizbuysell_companies.xlsx')
