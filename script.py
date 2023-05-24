from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from chromedriver_binary import chromedriver_filename
from selenium.common.exceptions import NoSuchElementException
import time

website = "https://www.google.com/"
webdriver_path = chromedriver_filename

try:
    service = Service(executable_path=webdriver_path)
    driver = webdriver.Chrome(service=service)

    # Prompt the user
    keyword = input("Search: ")

    def scrape(kw):
        try:
            # Navigate to the Google search page
            driver.get(website)

            search_input = driver.find_element(by="xpath", value='//textarea[@id="APjFqb"]')
            search_input.send_keys(kw)
            search_input.send_keys(Keys.RETURN)

            # Scroll to People also ask
            paa_element = driver.find_element(by="xpath", value='//div[@class="T6zPgb"]')
            driver.execute_script("arguments[0].scrollIntoView(true);", paa_element)

            # Change nav element style position fixed to absolute
            nav_element = driver.find_element(by="xpath", value='//div[@id="searchform"]')
            driver.execute_script("arguments[0].style.position = 'absolute';", nav_element)

            container_elements = driver.find_elements(by="xpath", value='//div[@jsname="YrZdPb"]')

            faqs = {}
            limit = 10

            # First iteration
            for container_element in container_elements:
                driver.execute_script("arguments[0].scrollIntoView(true);", container_element)

                driver.execute_script("arguments[0].style.position = 'absolute';", nav_element)

                time.sleep(5)
                container_element.click()

            question_elements = driver.find_elements(by="xpath", value='//div[@jsname="lN6iy"]')
            answer_elements = driver.find_elements(by="xpath", value='//div[@class="wDYxhc"]')
            blocks = driver.find_elements(by="xpath", value='//div[@jsname="NRdf4c"]/.')
            containers = driver.find_elements(by="xpath", value='//div[@jsname="YrZdPb"]/div[2]/div[@jsname="tJHJj"]')

            # Final iteration
            for index, (question_element, answer_element, block, container) in enumerate(zip(question_elements, answer_elements, blocks, containers)):

                if index == 0:
                    continue

                if index >= limit:
                    break

                question = question_element.find_element(by="xpath", value='./span[1]/span[1]').text
                display_property = block.value_of_css_property("display")

                xpath_options = [
                    ('./div[@class="LGOjhe"]/span[1]/span[1]/.', "LGOjhe"),
                    ('./div[@class="di3YZe"]/*', "di3YZe"),
                    ('./div[@class="Crs1tb"]/*', "Crs1tb")
                ]

                found_element = None

                if display_property == "none":
                    time.sleep(5)
                    container.click()

                for xpath, class_name in xpath_options:
                    try:
                        element = answer_element.find_element(by="xpath", value=xpath)
                        time.sleep(5)
                        answer = element.text
                        found_element = class_name
                        break
                    except NoSuchElementException:
                        continue
                
                if found_element is None:
                    print("No matching element found.")

                # try:
                #     answer_element.find_element(by="xpath", value='./div[@class="LGOjhe"]')
                #     print(answer_element.find_element(by="xpath", value='./div[@class="LGOjhe"]/span[1]/span[1]').text)
                # except NoSuchElementException:
                #     try:
                #         print(answer_element.find_element(by="xpath", value='./div[@class="di3YZe"]/*').text)
                #     except NoSuchElementException:
                #         print(answer_element.find_element(by="xpath", value='./div[@class="Crs1tb"]/*').text)

                # if display_property == "block":
                    # el = answer_element.find_element(by="xpath", value='./div[1]/*')
                    # answer = el.text
                    # print("block")

                # if display_property == "none": 
                    # container_locator = '//div[@jsname="YrZdPb"]/div[2]/div[@jsname="tJHJj"]'
                    # container = wait.until(EC.element_to_be_clickable((By.XPATH, container_locator)))
                    # time.sleep(5)
                    # container.click()
                    # el = answer_element.find_element(by="xpath", value='./div[1]/*')
                    # answer = el.text
                    # print("none")

                faqs[question] = answer

            print(faqs)

        except Exception as e:
            print("An error occurred:", str(e))

        finally:
            driver.quit()

    scrape(keyword)

except Exception as e:
    print("An error occurred:", str(e))
