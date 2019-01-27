from selenium import webdriver
import time


def before_all(context):

    if 1:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        context.browser = webdriver.Chrome(options=options)
    else:
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        context.browser = webdriver.Firefox(options=options)

    context.browser.implicitly_wait(1)
    context.server_url = 'http://localhost:8000'


def after_all(context):
    # Explicitly quits the browser, otherwise it won't once tests are done
    context.browser.quit()


def before_feature(context, feature):
    # Code to be executed each time a feature is going to be tested
    pass



#
#
# def before_all(context):
#
#     import selenium.webdriver.chrome.service as service
#     service = service.Service('/usr/local/bin/chromedriver')
#     service.start()
#     driver = webdriver.Remote(service.service_url)
#
#     # driver.get('http://www.google.com/xhtml');
#     # time.sleep(3)  # Let the user actually see something!
#
#     context.browser = driver
#     context.browser.implicitly_wait(1)
#     #context.browser.get('http://topia.com')
#     context.server_url = 'http://localhost:8000'
#     context.server_url = 'http://google.com'
#
#
# def after_all(context):
#     # Explicitly quits the browser, otherwise it won't once tests are done
#     context.browser.quit()
#
#
# def before_feature(context, feature):
#     # Code to be executed each time a feature is going to be tested
#     pass
