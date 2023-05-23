from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

website = "https://www.google.com/"
path = "/usr/bin/chromedriver"

try:
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)

    # Prompt the user
    keyword = input("Search: ")

    def scrape(kw):
        try:
            # Navigate to the Google search page
            driver.get(website)

            search_input = driver.find_element(by="xpath", value='//textarea[@class="gLFyf"]/.')
            search_input.send_keys(kw)
            search_input.send_keys(Keys.RETURN)

            container_elements = driver.find_elements(by="xpath", value='//div[@jsname="YrZdPb"]/.')
            nav_element = driver.find_element(by="xpath", value='//div[@class="CvDJxb"]/.')

            faqs = {}
            limit = 10

            # First iteration
            for container_element in container_elements:
                driver.execute_script("arguments[0].scrollIntoView(true);", container_element)
                driver.execute_script("arguments[0].style.position = 'absolute';", nav_element)

                wait = WebDriverWait(driver, 10)

                overlay_locator = '//div[@jsname="YrZdPb"]/div[2]/div[@class="dnXCYb"]'
                overlay = wait.until(EC.visibility_of_element_located((By.XPATH, overlay_locator)))
                driver.execute_script("arguments[0].remove();", overlay)

                element_locator = '//div[@jsname="YrZdPb"]/div[2]/div[@class="dnXCYb"]'
                element = wait.until(EC.element_to_be_clickable((By.XPATH, element_locator)))
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                driver.execute_script("arguments[0].style.position = 'absolute';", nav_element)
                time.sleep(5)
                element.click()

            question_elements = driver.find_elements(by="xpath", value='//div[@class="JlqpRe"]/.')
            answer_elements = driver.find_elements(by="xpath", value='//div[@class="wDYxhc"]/.')

            # Final iteration
            for index, (question_element, answer_element) in enumerate(zip(question_elements, answer_elements)):
                if index >= limit:
                    break

                question = question_element.find_element(by="xpath", value='./span[1]/span[1]/.').text

                block = driver.find_element(by="xpath", value='//div[@class="bCOlv"]/.')
                display_property = block.value_of_css_property("display")

                wait = WebDriverWait(driver, 10)

                if display_property == "block":
                    el = answer_element.find_element(by="xpath", value='./div[1]/*')
                    answer = el.text
                else:
                    container_locator = '//div[@jsname="YrZdPb"]/div[2]/div[@class="dnXCYb"]'
                    container = wait.until(EC.element_to_be_clickable((By.XPATH, container_locator)))
                    time.sleep(5)
                    container.click()
                    el = answer_element.find_element(by="xpath", value='./div[1]/*')
                    answer = el.text

                faqs[question] = answer

            print(faqs)

        except Exception as e:
            print("An error occurred:", str(e))

        finally:
            driver.quit()

    scrape(keyword)

except Exception as e:
    print("An error occurred:", str(e))