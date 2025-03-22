import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

from smolagents import tool

def random_delay(min_delay=2, max_delay=7):
    deltime = random.uniform(min_delay, max_delay)
    print(f'delay {deltime:.3} s')
    time.sleep(deltime)


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]

def get_random_user_agent():
    return random.choice(user_agents)

def random_delay(min_delay=3, max_delay=7):
    time.sleep(random.uniform(min_delay, max_delay))

def scroll_down(driver, min_scroll=200, max_scroll=500):
    scroll_height = random.randint(min_scroll, max_scroll)
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN)
    actions.perform()
    time.sleep(random.uniform(1, 3))



@tool
def search_tool(request: str) -> str:
    '''
    This tool can be used for search any query in the internet by browser.
    Args:
        request: literally request that you can type in browser line
    Returns:
        string that contatins 10 first results of web search with links to them
    '''
    options = webdriver.FirefoxOptions()
    options.add_argument(f"user-agent={get_random_user_agent()}")

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444',  # GeckoDriver
        options=options
    )
    try:
        # === Your Automation Code ===
        driver.get("https://duckduckgo.com/")
        random_delay()

        # Find search box and enter query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(request)
        print('search request: ', request)
        random_delay()

        # Submit the query
        search_box.send_keys(Keys.RETURN)
        random_delay()

        # Scroll down the page
        scroll_down(driver)

        # find the result container
        results_container = driver.find_element(By.CSS_SELECTOR, "ol.react-results--main")

        results = results_container.find_elements(By.CSS_SELECTOR, "li[data-layout='organic']") # first element link with results

        final_res = ''
        for result in results:
            try:
                h2_tag = result.find_element(By.CSS_SELECTOR, "h2")

                a_tag = h2_tag.find_element(By.CSS_SELECTOR, "a")

                title = a_tag.find_element(By.CSS_SELECTOR, "span").text

                link = a_tag.get_attribute("href")

                final_res += f"Title: {title}\n"
                final_res += f"Link: {link}\n"
                final_res += "-" * 20 + '\n'
                random_delay(0.1, 1)
            except Exception as inner_e:
                print(f"error: {inner_e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
        return final_res