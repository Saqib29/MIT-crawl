from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from chrome_option import chrome_option
import time
import datetime
import re 
import logging

from functions import data_collect_function, pick_date_function, load_page_function, total_rows_function, total_result_function 

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EMA(1) indices scrapper")
logger.setLevel(logging.INFO)

url = 'https://www.ema.europa.eu/en/news-events/whats-new'



def get_indices(fromDate, todate):
    logger.info('driver started')

    options = chrome_option()

    while True:
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())#, options=options)
            break
        except Exception:
            logger.info("Internet connection problem")
            time.sleep(5)

    driver.get(url)

    # Select date
    from_date = fromDate[:7]

    rows = total_contents(driver)
    total_results = driver.execute_script(from_date.join(total_result_function.split("[dynamic]")))
    total_results = int(total_results[1:-1])
    print(total_results)

    
    driver.execute_script(from_date.join(pick_date_function.split("[dynamic]")))
    time.sleep(2)

    # rows = total_contents(driver)
    # total_results = driver.execute_script(from_date.join(total_result_function.split("[dynamic]")))
    # total_results = int(total_results[1:-1])
    # print(total_results)

    while True:
        if rows >= total_results:
            break
        driver.execute_script(load_page_function)
        time.sleep(5)
        rows = total_contents(driver)
        
    all_links = crawling_data(driver)
    
    # here date range will be checked

    driver.close()
    return all_links


def crawling_data(driver):
    all_links = driver.execute_script(data_collect_function)
    return all_links


def total_contents(driver):
    rows = driver.execute_script(total_rows_function)
    return rows


if __name__ == '__main__':
    fromDate = "2021-06-15"
    toDate = "2021-06-21"

    results = get_indices(fromDate, toDate)
    
    # for data in results:
    #     print(data)
    
    print(len(results))
    


