# Selenium爬取淘宝商品信息
1. 使用工具： Python3 + selenium  
2. 进入淘宝，搜索iPad, 网址： https://s.taobao.com/search?q=iPad
目的获得如下类型的商品信息  
![图一](https://www.baidu.com/img/bd_logo1.png?where=super)  
3. 在页面下方有个分页导航，要获取每一页的商品信息只需要遍历1到100页即可， 在这里不通过点击下一页进行遍历，而是**选择在页面跳转的文本框中输入页码进行遍历**， 这样的**好处**是：如果选择点击下一页的话，一旦跳转页面时出现错误，就无法接着本页面继续向后跳转，而选择输入页码则可以随时进入任一页进行抓取。
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
定位到页码输入框与确定按钮，右键点击检查，定位到元素位置，![图2](https://www.baidu.com/img/bd_logo1.png?where=super)
        
