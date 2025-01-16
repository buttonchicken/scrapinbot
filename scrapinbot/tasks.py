# tasks.py
from celery import shared_task
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

@shared_task
def scrape_products(url):
    '''
    Parameters - > url of the site to be scraped
    Returns -> list of product urls scrapped
    '''
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url) 
        time.sleep(10)
        elements = driver.find_elements(By.TAG_NAME, "div")
        class_name_mapping = {}
        for element in elements:
            class_name = element.get_attribute('class')
            if class_name not in class_name_mapping:
                class_name_mapping[class_name] = 1
            else:
                class_name_mapping[class_name] += 1
        if len(class_name_mapping) == 0:
            return None
        else:
            filtered_mapping = {k: v for k, v in class_name_mapping.items() if 12 <= v <= 40}
            sorted_mapping = sorted(filtered_mapping.items(), key=lambda x: x[1])
            urls = []
            for class_name, freq in sorted_mapping:
                all_elements = driver.find_elements(By.CLASS_NAME,class_name)
                WebDriverWait(driver, 10)
                for element in all_elements:
                        try:
                            element.click()
                            WebDriverWait(driver, 10)
                            driver.switch_to.window(driver.window_handles[-1])
                            urls.append(driver.current_url)
                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            continue
                if len(urls)>=12:
                    break
            driver.quit()
            return urls
    except Exception as e:
        print(f"Error scraping URL {url}: {e}")
        return None
