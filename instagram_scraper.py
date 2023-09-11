import os

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup as soup

# Selenium params
timeout = 120

TEST = False


def open_chrome_browser(url: str = None) -> webdriver:
    if TEST:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=ChromeService("drivers/chromedriver-win64.exe"),options=chrome_options)
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)

    if url:
        driver.get(url)

    return driver


def handle_cookies(driver: webdriver) -> webdriver:
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Decline optional cookies')]")))
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Decline optional cookies')]")
        button.click()

    except NoSuchElementException:
        print(f"No cookies to handle for {driver.current_url}")

    except Exception as e:
        print("Exception thrown handling cookies")
        print(e)

    return driver


def fetch_max_posts_without_account(driver: webdriver) -> webdriver:
    # TODO: click show more posts button
    try:
        pass
        # WebDriverWait(driver, timeout).until(
        #     EC.visibility_of_all_elements_located((By.CLASS_NAME, show_more_posts_button_class_name)))
        # button = driver.find_element(By.CLASS_NAME, show_more_posts_button_class_name)
        # button.click()
    except Exception as e:
        print("Exception thrown clicking show more posts button")
        print(e)


def get_post_links_via_html_tags(driver: webdriver) -> (webdriver, list[str]):
    page_src = driver.page_source
    page_soup = soup(page_src, "html.parser")

    post_links = []

    for item in page_soup.find_all("a"):  # fall under the a tag
        if "href" in item.attrs:
            #NOTE: IP sensitive part removed - but this is where the relevant post link is selected
            pass

    print(f"found {len(post_links)} individual posts")

    return driver, post_links


#NOTE: not used to scrape but a possible way to do it
def get_post_links_via_javascript(driver: webdriver) -> (webdriver, list[str]):

    page_src = driver.page_source
    page_soup = soup(page_src, "html.parser")

    # find all property ids with value "Post Shortcode" & use their corresponding values as post links
    post_links = []
    for item in page_soup.find_all("script"):  # fall under the javascript tag
        if "Post Shortcode" in item.text:
            target_script = item.text
            occurrences_of_key = find_all_occurences(target_script, "Post Shortcode")
            print(occurrences_of_key)

            # NOTE: not used due to manual settinn in following code
            for occurrence in occurrences_of_key:
                print(target_script[occurrence - 15: occurrence + 38])
                post_links.append(target_script[occurrence - 15: occurrence + 38])

    print(f"found {len(post_links)} individual posts")
    print(post_links)

    return driver, post_links


def get_description_and_image_from_post(driver: webdriver, post_link: str, scrape_image=True) -> tuple[str, str]:
    full_link = f"https://www.instagram.com{post_link}"

    try:
        driver.get(full_link)
        handle_cookies(driver)
        page_src = driver.page_source
        page_soup = soup(page_src, "html.parser")

        # get meta properties - this contains the description
        # NOTE: left this in as it is fairly trivial to get the description from the meta properties
        description_from_meta_properties = page_soup.findAll("meta", {"property": "og:title"})
        if len(description_from_meta_properties) > 0:
            description_from_meta_properties = description_from_meta_properties[0].get("content")

        # get all images on page
        if scrape_image:
            # get all srcset attributes from img tags
            images = page_soup.findAll("img")
            # NOTE: IP sensitive part removed - but this is where the relevant post image is selected

        return description_from_meta_properties, None

    except Exception as e:
        print("Exception thrown getting description from dynamic page")
        print(e)


def find_all_occurences(string: str, substring: str) -> list[int]:
    occurences = []
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            return occurences
        occurences.append(start)
        start += len(substring)  # use start += 1 to find overlapping occurences

def overall_description_and_picture_scraper(username: str) -> list[tuple[str, str, str]]:
    url = f"https://www.instagram.com/{username}/"
    print(f"scraping {url}")
    scraped_data = []
    with open_chrome_browser(url) as chrome_driver:
        print(f"opened {url} on the chrome browser")
        handle_cookies(chrome_driver)
        print(f"handled cookies")
        _, post_links = get_post_links_via_html_tags(chrome_driver)
        for post_link in post_links:
            description, image_url = get_description_and_image_from_post(chrome_driver, post_link)
            if image_url is not None:
                image_url = image_url.split(' ')[0] # since srcset contains multiple urls for different sizes
                print(f"image url: \n{image_url.split(' ')[0]}")
            scraped_data.append((post_link, description, image_url))

    return scraped_data

# for testing
if __name__ == "__main__":
    overall_description_and_picture_scraper("heavenlyddesserts")
