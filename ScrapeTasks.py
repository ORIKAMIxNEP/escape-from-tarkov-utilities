import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

tradersList = []
driver.get("https://wikiwiki.jp/eft/")
traders = driver.find_elements(
    By.XPATH, value="//*[@id='menubar']/ul[2]/li[7]/ul/li/a")
for trader in traders:
    if trader.text != "Fence":
        tradersList.append(trader.text)

taskURLs = {traderName: [] for traderName in tradersList}
for traderName in tradersList:
    driver.get("https://wikiwiki.jp/eft/" + traderName)
    tasks = driver.find_elements(
        By.XPATH, value="//*[@id='content']/ul[1]/li/a")
    for task in tasks:
        taskURLs[traderName].append(task.get_attribute("href"))

spreadsheetsData = ""
taskCount = {traderName: {"allCount": 0, "validCount": 0}
             for traderName in tradersList}
errorTaskPages = []
for traderName in tradersList:
    spreadsheetsData += traderName + "\n"
    for taskURL in taskURLs[traderName]:
        taskCount[traderName]["allCount"] += 1
        driver.get(taskURL)
        try:
            taskName = driver.find_element(
                By.XPATH, value="//*[@id='title']/h1").text
            if "/" in taskName:
                taskName = taskName[taskName.index("/") + 1:]
            kappaRequired = driver.find_element(
                By.XPATH, value="//*[@id='content']//td[contains(text(), 'Kappaタスク')]/following-sibling::td[1]").text
        except:
            errorTaskPages.append(taskURL)
            continue
        taskCount[traderName]["validCount"] += 1
        spreadsheetsData += taskName + "\t" + kappaRequired + "\n"

for traderName in tradersList:
    print(traderName + "'s AllTaskPage: " +
          str(taskCount[traderName]["allCount"]))
    print(traderName + "'s ValidTaskPage: " +
          str(taskCount[traderName]["validCount"]))

print("エラータスクページ：", end="")
for i, errorTaskPage in enumerate(errorTaskPages):
    if i == len(errorTaskPages) - 1:
        print(errorTaskPage)
    else:
        print(errorTaskPage, end=", ")

pyperclip.copy(spreadsheetsData)
print("スプレッドシート用のデータをクリップボードにコピーしました。")

driver.quit()
