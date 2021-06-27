from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from chrome_option import chrome_option
from datetime import datetime
import time
import logging

from functions import data_collect_function, pick_date_function, load_page_function, total_rows_function, total_result_function 

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EMA(1) indices scrapper")
logger.setLevel(logging.INFO)

url = 'https://www.ema.europa.eu/en/news-events/whats-new'



def get_indices(searchItem, fromDate, todate):
    logger.info('driver started')

    options = chrome_option()

    while True:
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            break
        except Exception:
            logger.info("Internet connection problem")
            time.sleep(5)

    driver.get(url)

    # Select date
    from_date = fromDate[:7] #"2021-06"

    # get total results count of the month from block_content
    try:
        total_results = driver.execute_script(from_date.join(total_result_function.split("[dynamic]")))
        total_results = int(total_results[1:-1])
        logger.info("Total results found "+ str(total_results))
    except Exception as e:
        logger.error(f"Content doesn't exists for this date {fromDate}")
        logger.error(e)
        return list()
        
    # clicking on the month date need to crawl
    try:
        driver.execute_script(from_date.join(pick_date_function.split("[dynamic]")))
        time.sleep(2)
    except Exception as e:
        logger.error(f"Content doesn't exists for this date {fromDate}")
        logger.error(e)
        return list()

    try:
        rows = total_contents(driver)
        while True:
            if rows >= total_results:
                break
            driver.execute_script(load_page_function)
            time.sleep(2)
            rows = total_contents(driver)
    except Exception as e:
        logger.error(e)
        
    
    # all data crawling 
    all_links = crawling_data(driver)
    # filtering date and search string
    filtered_data = filter_links(all_links, searchItem, fromDate, todate)


    driver.close()
    return filtered_data


def crawling_data(driver):
    try:
        all_links = driver.execute_script(data_collect_function)
        return all_links
    except Exception as e:
        logger.error(e)
        return list()


def total_contents(driver):
    rows = driver.execute_script(total_rows_function)
    return rows


def filter_links(all_links, searchItem, fromDate, todate):
    if len(all_links) == 0:
        return list()
    
    try:
        from_date = datetime.strptime(fromDate, '%Y-%m-%d')
        to_date = datetime.strptime(todate, '%Y-%m-%d')

        data = []
        for content in all_links:
            curr_date = datetime.strptime(content["date"], "%d/%m/%Y")
            if from_date <= curr_date and curr_date <= to_date:
                if searchItem.capitalize() in content["content"] or searchItem.lower() in content["content"]:
                    data.append(content)
            
        return data
    except Exception as e:
        logger.error(e)
        return list()





if __name__ == '__main__':
    fromDate = "2021-06-15"
    toDate = "2021-06-25"
    searchItem = "Human"

    results = get_indices(searchItem, fromDate, toDate)
    
    # for data in results:
    #     print(data)
    
    logger.info(str(len(results)) + f" results found for search item {searchItem} in date range {fromDate} to {toDate}")
    


