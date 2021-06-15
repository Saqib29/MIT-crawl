from selenium.webdriver.chrome.options import Options


def chrome_option() -> Options:
    """ Sets chrome option for Selenium.
    Chrome option for headless brawser is enebled. 
    """

    option = Options()
    # Dont change these options
    option.add_argument('--headless')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--no-sandbox')

    return option
