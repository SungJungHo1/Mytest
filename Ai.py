from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

options = webdriver.ChromeOptions()
# options.add_argument("window-size=1920x1080")
# options.add_experimental_option(
#     "excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--incognito")

driver = webdriver.Chrome()
driver.implicitly_wait(10)
url = "https://race.kra.co.kr/raceScore/scoretablePeriodScoreList.do"
YY = 2023
Stop_YY = 2015

while YY >= Stop_YY:
    driver.get(url)
    기간검색 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[@type='button']//span[contains(text(),'기간별검색')]")))
    # 년 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//select[@id='arg_Year1']/option[text()='2023']")))
    # 월 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//select[@name='arg_Mon1']/option[text()='01']")))
    # 일 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//select[@name='arg_Day1']/option[text()='01']")))
    # 검색 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button[@type='button']//span[contains(text(),'검색')]")))

    driver.find_element(By.XPATH,"//button[@type='button']//span[contains(text(),'기간별검색')]").click()
    driver.find_element(By.XPATH,f"//select[@id='arg_Year1']/option[text()={str(YY)}]").click()
    driver.find_element(By.XPATH,f"//select[@name='arg_Mon1']/option[text()=01]").click()
    driver.find_element(By.XPATH,f"//select[@name='arg_Day1']/option[text()=01]").click()
    driver.find_element(By.XPATH,f"//select[@id='arg_Year2']/option[text()={str(YY)}]").click()
    driver.find_element(By.XPATH,f"//select[@name='arg_Mon2']/option[text()=12]").click()
    driver.find_element(By.XPATH,f"//select[@name='arg_Day2']/option[text()=30]").click()
    driver.find_element(By.XPATH,"//button[@type='button']//span[contains(text(),'검색')]").click()
    length = len(driver.find_elements(By.XPATH,"//table//td[@class='alignL']//a"))
    time.sleep(1)
    count = 0
    columns=[['순위', '마번', '마명', '산지', '성별', '연령', '중량', '레이팅', '기수명', '조교사명', '마주명', '도착차', '마체중', '단승', '연승', '장구현황'],
    ['순위', '마번','S1F-1C-2C-3C-G3F-4C-G1F', 'S1F 지점', '1코너 지점',  '2코너 지점', '3코너 지점', 'G3F 지점', '4코너 지점', 'G1F 지점', '3F-G', '1F-G','경주 기록']]
    while True:
        try:
            for i in range(length):
                find_as = driver.find_elements(By.XPATH,"//table//td[@class='alignL']//a")
                find_as[i].click()
                to_add_text = driver.find_element(By.XPATH,"//div[@class='tableType1']").text
                print(to_add_text)
                
                contents_s = []
                
                for idx,k in enumerate(driver.find_elements(By.XPATH,"//div[@class='tableType2']//tbody")[:2]):
                    rows=k.find_elements(By.CSS_SELECTOR,"tr")
                    rows_contents=[]
                    for row in rows:
                        contents = row.find_elements(By.CSS_SELECTOR,"td")
                        contents_text = [content.text for content in contents]
                        rows_contents.append(contents_text)
                    contents_s.append(pd.DataFrame(rows_contents,columns=columns[idx-2]))
                # time.sleep(1)
                total_data = pd.concat([contents_s[0],contents_s[1]],axis=1,ignore_index=True)
                total_data['added_feature']=to_add_text
                count+=1
                total_data.to_csv(f'C:/Users/user/Desktop/AI/실험{str(count)}.csv',encoding='ms949')
                driver.execute_script("window.history.go(-1)")
                
            driver.find_element(By.XPATH,"//button[@type='button']//span[contains(text(),'다음')]").click()

        except :
            print("end")
            break
