import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import platform

def vaccine_status(html):
    html = html.find("div", {"class" : "_20WMD"})
    html = html.find("div").find("div").find("div").find("div")
    html = html.find_all("div", {"class" : "dvng-"})

    hospital = []
    leftover_vaccine_len = []
    for i in html:
        hospital.append(i.find("span", {"class" : "place_blind"}).get_text().replace("개", ""))
        leftover_vaccine_len.append(i.find("div", {"class" : "_3sd6u"}).get_text())

    return hospital, leftover_vaccine_len


if __name__ == "__main__":
    # 변수설정
    version = "1.0"
    now_folder = os.getcwd()
    path_drive = now_folder + "/chromedriver"
    vaccine_url = "https://m.place.naver.com/rest/vaccine?vaccineFilter=used"

    # DRIVER_SETTING
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    cap = DesiredCapabilities().CHROME
    cap["marionette"] = True
    
    # 셀레니움 크롬 열기
    driver = webdriver.Chrome(executable_path=path_drive)
    #driver = webdriver.Chrome(executable_path=path_drive, options=options)
    driver.get(vaccine_url)
    driver.implicitly_wait(10)
    time.sleep(10)
    # GPS 버튼
    try:
        driver.find_element_by_xpath('//*[@id="app-root"]/div/div/div[2]/div/div/a[@class="_3_X4H _1dUVm"]').click()
    except:
        pass
    time.sleep(3)
    # 지도 검색
    try:
        driver.find_element_by_xpath('//*[@id="app-root"]/div/div/div[2]/div/a[@class="_2v3t_"]').click()
    except:
        pass
    time.sleep(3)

    while True:
        vaccine_html = driver.page_source
        vaccine_html_bs = BeautifulSoup(vaccine_html, 'lxml')

        hospital, leftover_vaccine_len = vaccine_status(vaccine_html_bs)

        for i in range(len(leftover_vaccine_len)):
            now_v = leftover_vaccine_len[i]
            if now_v != "마감" and now_v != "대기중" and now_v != "0":
                if platform.system() == "Darwin":
                    from pync import Notifier
                    Notifier.notify(hospital[i], title='잔여 백신 알림')
                print(hospital[i])

        driver.find_element_by_class_name('_1MCHh').click()
        time.sleep(3)