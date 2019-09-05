from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def gen_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/bin/google-chrome-beta"

    prefs = {"download.default_directory": "/home/sss/dev/python/19-08-22_MakeWeatherGreatAgain/download/"}
    # prefs = {"downloadPath" : "/home/sss/dev/python/19-08-22_MakeWeatherGreatAgain/download/"}
    chrome_options.add_experimental_option("prefs", prefs)

    # Чтобы работала в фоне
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def download_file(driver):
    print('start')

    driver.get(
        "https://rp5.ru/%D0%90%D1%80%D1%85%D0%B8%D0%B2_%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D1%8B\
        _%D0%B2_%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5_(%D0%92%D0%94%D0%9D%D0%A5)")
    elem = driver.find_element_by_id('tabSynopDLoad')
    time.sleep(1)
    elem.click()
    elem = driver.find_element_by_id('calender_dload')
    elem.clear()
    elem.send_keys('01.01.2019')
    elem.send_keys(Keys.RETURN)
    elem = driver.find_element_by_id('calender_dload2')
    elem.clear()
    elem.send_keys('01.02.2019')
    elem.send_keys(Keys.RETURN)
    driver.find_element_by_xpath("//div[@id='toFileMenu']/form/table[2]/tbody/tr[2]/td[3]/label").click()
    driver.find_element_by_xpath(
        u"(.//*[normalize-space(text()) and normalize-space(.)='Выбрать в файл GZ (архив)'])\
        [1]/preceding::label[2]").click()
    driver.find_element_by_xpath(
        u"(.//*[normalize-space(text()) and normalize-space(.)='—'])[2]/preceding::div[2]").click()
    time.sleep(3)
    elem = driver.find_element_by_link_text(u"Скачать").click()
    time.sleep(5)
    print('end')

    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    driver.close()


def main():
    driver = gen_options()
    download_file(driver)


if __name__ == '__main__':
    main()
