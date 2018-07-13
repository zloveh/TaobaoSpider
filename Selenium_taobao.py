# -*- coding: utf-8 -*-
from selenium import webdriver

# 导入期望类
from selenium.webdriver.support import expected_conditions as EC

# 导入By类
from selenium.webdriver.common.by import By

# 导入显式等待类
from selenium.webdriver.support.wait import WebDriverWait

# 导入异常类
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import pymongo


driver = webdriver.Chrome()
# 无头
# opn = webdriver.ChromeOptions()
# opn.set_headless()
# driver = webdriver.Chrome(options=opn)
wait = WebDriverWait(driver, 20, 0.5)
KEYWORD = "iPad"
MAX_PAGE = 100

MONGO_URL = "localhost"
MONGO_DB = "taobao"
MONGO_COLLECTION = "product"


def index_page(page):
    """
    抓取索引页面
    :param page: 页码
    :return:
    """
    print(f"正在爬取{page}页")
    try:
        url = "https://s.taobao.com/search?q=" + KEYWORD
        driver.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#mainsrp-pager div.form > input")
                )
            )
            submit = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#mainsrp-pager div.form > span.btn.J_Submit")
                )
            )
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#mainsrp-pager li.item.active > span"), str(page)
            )
        )
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".m-itemlist .items .item")
            )
        )
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    """
    提取商品数据
    :return:
    """
    html = driver.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            "image": item.find(".pic .img").attr("data-src"),
            "price": item.find(".price").text(),
            "deal": item.find(".deal-cnt").text(),
            "title": item.find(".title").text(),
            "shop": item.find(".shop").text(),
            "location": item.find(".location").text(),
        }
        print(product)
        save_mongo(product)


def save_mongo(product):
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    try:
        if collection.insert_one(product):
            print("存储到MongoDB成功")
    except:
        print("存储失败")


def main():
    """
    遍历每一页
    :return:
    """
    for page in range(1, MAX_PAGE + 1):
        index_page(page)
        # break                   # 便于调试


if __name__ == "__main__":
    main()
