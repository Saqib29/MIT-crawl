from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from chrome_option import chrome_option
import time
import re 

url = 'https://www.ema.europa.eu/en/news-events/whats-new'

options = chrome_option()

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(url)
# driver.refresh()

def load_page():
    load = driver.find_element_by_xpath("//a[normalize-space()='Load more']")
    driver.execute_script('arguments[0].click();', load)
    time.sleep(20)


def collect_rows():
    table = driver.find_element_by_xpath("//body//main//table[2]//tbody")
    rows = driver.execute_script("return document.getElementsByTagName('tr').length")
    return rows



last_update = driver.find_element_by_xpath('//a[13]')
driver.execute_script('arguments[0].click();', last_update)

last_update = driver.find_element_by_xpath('//a[13]')
total_results = re.search(r"\(\d+\)" ,last_update.text)
total_results = int(total_results.group(0)[1:-1])
print(total_results)


rows = collect_rows()
if rows < total_results:
    load_page()
    rows = collect_rows()


print(rows)

for row in range(1,rows-1):
    r = driver.execute_script(f'return document.querySelector("tbody tr:nth-child({row})")')
    print(f"{row}  -> "+r.text)

    # if row > 10:
    #     break

driver.close()