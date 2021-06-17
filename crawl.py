from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from chrome_option import chrome_option
import time
import datetime
import re 
import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EMA(1)")
logger.setLevel(logging.INFO)


url = 'https://www.ema.europa.eu/en/news-events/whats-new'

options = chrome_option()
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get(url)


def load_page():
    # load = driver.find_element_by_xpath("//a[normalize-space()='Load more']")
    load = driver.execute_script("""return document.querySelector("body main div div section div div ul li a")""")
    driver.execute_script('arguments[0].click();', load)
    logger.info("Page load exists")
    time.sleep(20)


def collect_rows():
    rows = driver.execute_script("return document.getElementsByTagName('tr').length")
    return rows


month = str(datetime.datetime.now())[:7]
# last_update = driver.find_element_by_xpath('//a[13]')
last_update = driver.execute_script(f"""return document.querySelector("a[href='/en/news-events/whats-new/{month}']")""")
driver.execute_script('arguments[0].click();', last_update)

last_update = driver.execute_script(f"""return document.querySelector("a[href='/en/news-events/whats-new/{month}']")""")
total_results = re.search(r"\(\d+\)" ,last_update.text)
total_results = int(total_results.group(0)[1:-1])


print(total_results)
rows = collect_rows()
if rows < total_results:
    load_page()
    rows = collect_rows()
print(rows)
logger.info("Data collected")


date_contents = []

for row in range(1,rows-1):
    # r = driver.execute_script(f'return document.querySelector("tbody tr:nth-child({row})")')
    date = driver.execute_script(f'return document.querySelector("tbody tr:nth-child({row}) td:nth-child(1)")').text
    content = driver.execute_script(f'return document.querySelector("tbody tr:nth-child({row}) td:nth-child(2)")')
    link = content.find_element_by_tag_name("a").get_attribute("href")
    
    date_contents.append({
        "date" : date,
        "content" : content.text,
        "datalink" : link
    })
    
    

    # if row > 10:
    #     break

logger.info("crawl finished")
driver.close()

count = 1
for data in date_contents:
    print(f"{count} -> ", data)
    count += 1  