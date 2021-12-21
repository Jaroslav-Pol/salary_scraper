'''
Tasks:
Create scraper that takes position, salary, company
Then create search engine to search salary by position
Create web page for user
'''

'''
This scraper takes data from cvbankas.lt from all pages from the search. 
To make things work just copy link from cvbankas search by something(without page number) to base_url. 
Then change file name 
'''
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from random import randint

driver = webdriver.Chrome(executable_path='C:/Users/jaros/Desktop/Python/WebScraping/chromedriver.exe')
base_url = 'https://www.cvbankas.lt/?padalinys%5B0%5D=76&page='
result_dic = {'position': [],
              'company': [],
              'salary range': [],
              'brutto': []
              }

def last_page():
    """returns last page of the current search (in cvbankas.lt)"""
    driver.get(base_url + '1')  # adds page number
    content = driver.page_source
    soup = BeautifulSoup(content)

    html_elements = soup.find(class_='pages_ul_inner').find_all('a')
    return int(html_elements[-1].text)


for page in range(last_page()):
    '''This loop is going through all pages of the search'''
    time.sleep(randint(1, 5))

    page_results = []
    new_url = base_url + str(page + 1)
    print(new_url)

    driver.get(new_url)
    content = driver.page_source
    soup = BeautifulSoup(content)

    for a in soup.find_all(class_='list_a_wrapper'):
        '''list_a_wrapper class has all info we need'''
        try:
            position = a.find(class_='list_h3').text
            company = a.find(class_='dib mt5').text
            salary_range = a.find(class_='salary_amount').text
            if a.find(class_='salary_calculation').text == 'Neatskaičius mokesčių':
                brutto = True
            else:
                brutto = False
            page_results.append([position, company, salary_range, brutto])
        except:
            continue

    print(page_results)

    for result in page_results:
        '''Adding results to dictionary'''
        result_dic['position'].append(result[0])
        result_dic['company'].append(result[1])
        result_dic['salary range'].append(result[2])
        result_dic['brutto'].append(result[3])

driver.quit()
print(result_dic)

df = pd.DataFrame(result_dic)
df.to_csv('salaries5.csv', index=False, encoding='utf-8')

print('labas')
