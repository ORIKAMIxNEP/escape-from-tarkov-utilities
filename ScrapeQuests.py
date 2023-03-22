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

questURLs = {traderName: [] for traderName in tradersList}
for traderName in tradersList:
    driver.get("https://wikiwiki.jp/eft/" + traderName)
    quests = driver.find_elements(
        By.XPATH, value="//*[@id='content']/ul[1]/li/a")
    for quest in quests:
        questURLs[traderName].append(quest.get_attribute("href"))

spreadsheetsData = ""
questCount = {traderName: {"allCount": 0, "validCount": 0}
              for traderName in tradersList}
errorQuestPages = []
for traderName in tradersList:
    spreadsheetsData += traderName + "\n"
    for questURL in questURLs[traderName]:
        questCount[traderName]["allCount"] += 1
        driver.get(questURL)
        try:
            questName = driver.find_element(
                By.XPATH, value="//*[@id='title']/h1").text
            if "/" in questName:
                questName = questName[questName.index("/") + 1:]
            kappaRequired = driver.find_element(
                By.XPATH, value="//*[@id='content']//td[contains(text(), 'Kappaタスク')]/following-sibling::td[1]").text
        except:
            errorQuestPages.append(questURL)
            continue
        questCount[traderName]["validCount"] += 1
        spreadsheetsData += questName + "\t" + kappaRequired + "\n"

for traderName in tradersList:
    print(traderName + "'s AllQuestPage: " +
          str(questCount[traderName]["allCount"]))
    print(traderName + "'s ValidQuestPage: " +
          str(questCount[traderName]["validCount"]))

print("エラータスクページ：", end="")
for i, errorQuestPage in enumerate(errorQuestPages):
    if i == len(errorQuestPages) - 1:
        print(errorQuestPage)
    else:
        print(errorQuestPage, end=", ")

pyperclip.copy(spreadsheetsData)
print("スプレッドシート用のデータをクリップボードにコピーしました。")

driver.quit()
