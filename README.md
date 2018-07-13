# Selenium爬取淘宝商品信息
1. 使用工具： Python3 + selenium  
2. 进入淘宝，搜索iPad, 网址： https://s.taobao.com/search?q=iPad
目的获得如下类型的商品信息  
![图一](https://github.com/zloveh/TaobaoSpider/blob/master/image/1.png)  
3. 在页面下方有个分页导航，要获取每一页的商品信息只需要遍历1到100页即可， 在这里不通过点击下一页进行遍历，而是**选择在页面跳转的文本框中输入页码进行遍历**， 这样的**好处**是：如果选择点击下一页的话，一旦跳转页面时出现错误，就无法接着本页面继续向后跳转，而选择输入页码则可以随时进入任一页进行抓取。  
![图2](https://github.com/zloveh/TaobaoSpider/blob/master/image/7.png)
4. 进行索引页面的抓取：  
创建webdriver对象,并且使用显示等待  
    driver = webdriver.Chrome()     
    wait = WebDriverWait(driver, 20, 0.5)  
也可以创建无头浏览器对象  
        opn = webdriver.ChromeOptions()  
        opn.set_headless()  
        driver = webdriver.Chrome(options=opn)    
请求网页：  
    url = "https://s.taobao.com/search?q=" + KEYWORD  
    driver.get(url)  
定位到页码输入框与确定按钮，右键点击检查，定位到元素位置，![图2](https://github.com/zloveh/TaobaoSpider/blob/master/image/2.png)  
```  
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
```  
5. 判断页面是否跳转成功  
通过判断页码是否在存贮页码的节点中，和商品信息节点中是否存在商品  
![图3](https://github.com/zloveh/TaobaoSpider/blob/master/image/3.png)  
```  
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
```  
当确定页面跳转成功并且商品信息已经加载出来就对商品进行解析get_products()，并且还要对上述代码进行try-except检测， 出现异常则要重新输入页码进行解析， 这样可以保证程序不会出现终止。  
6. 解析页面   
采用pyquery解析出商品信息：  
```
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
```  
这里把解析出的商品信息构造成一个字典， 便于向MongoDB数据库存储  
7. MongoDB存储信息  
导入mongo模块, 配置基本信息   
```  
import pymongo
MONGO_URL = "localhost"
MONGO_DB = "taobao"
MONGO_COLLECTION = "product"

def save_mongo(product):
    client = pymongo.MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    try:
        if collection.insert_one(product):
            print("存储到MongoDB成功")
    except:
        print("存储失败")
```  
8. 循环遍历爬取每一页商品信息  
```  
def main():
    """
    遍历每一页
    :return:
    """
    for page in range(1, MAX_PAGE + 1):
        index_page(page)
        # break                   # 便于调试

```  
成果：  
![1](https://github.com/zloveh/TaobaoSpider/blob/master/image/5.png)  
![2](https://github.com/zloveh/TaobaoSpider/blob/master/image/6.png)  
***完整代码： Selenium_taobao.py***
