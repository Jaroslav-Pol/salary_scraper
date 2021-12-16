"""
Tasks:
Create scraper that takes position, salary, company
Then create search engine to search salary by position
Create web page for user

"""
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

#
driver = webdriver.Chrome(executable_path='C:/Users/jaros/Desktop/Python/WebScraping/chromedriver.exe')
base_url = 'https://www.cvbankas.lt/?padalinys%5B0%5D=76&page='
results = []
result_dic = {'position': [],
              'company': [],
              'salary range': [],
              'bruto': []
              }


def last_page():
    """returns last page of the current search (in cvbankas.lt)"""
    driver.get(base_url + '1')  # adds page number
    content = driver.page_source
    soup = BeautifulSoup(content)
    driver.quit()
    html_elements = soup.find(class_='pages_ul_inner').find_all('a')
    return int(html_elements[-1].text)


# for page in range(last_page()):
#     time.sleep(3)
#     new_url = base_url + str(page + 1)
#     print(new_url)

driver.get(base_url + '1')
content = driver.page_source
soup = BeautifulSoup(content)
driver.quit()

for a in soup.find_all(class_='list_a_wrapper'):
    position = a.find(class_='list_h3').text
    company = a.find(class_='dib mt5').text
    salary_range = a.find(class_='salary_amount').text
    if a.find(class_='salary_calculation').text == 'Neatskaičius mokesčių':
        bruto = True
    else:
        bruto = False
    results.append([position, company, salary_range, bruto])

print(results)

for element in results:
    result_dic['position'].append(element[0])
    result_dic['company'].append(element[1])
    result_dic['salary range'].append(element[2])
    result_dic['bruto'].append(element[3])

print(result_dic)
df = pd.DataFrame(result_dic)
df.to_csv('salaries2.csv', index=False, encoding='utf-8')
