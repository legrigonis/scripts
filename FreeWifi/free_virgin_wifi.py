from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from utils import random_mac, connect_hotspot
import random
import time
import requests

HEADLESS_LOGIN = False
LOGIN_ENDPOINT = "http://virgintrainseastcost.on.icomera.com/"


def virgin_portal_login():
    '''
    Automates login-page navigation, enables free 15 minutes of internet access.
    '''
    random_string = str(random.choice([i for i in xrange(100)]))

    if HEADLESS_LOGIN:
        driver = webdriver.PhantomJS('phantomjs')
    else:
        driver = webdriver.Firefox()

    driver.get(LOGIN_ENDPOINT)

    logged_in = True
    try:
        email_field = driver.find_element_by_name("tb_email")
        if email_field:
            print "\t-> Entering random email.."
            email_field.send_keys("east{}@gm.com".format(random_string))
            email_field.send_keys(Keys.RETURN)

        print "\t-> Selecting free 15min Wi-Fi option"
        free_wifi_button = driver.find_element_by_id("btn15Min")
        free_wifi_button.send_keys(Keys.RETURN)
    except Exception:
        logged_in = False
        pass

    driver.close()
    return logged_in


def free_wifi():
    '''
    Changes mac address, connects to hotspot and grabs free 15 minutes.
    '''
    print "Changing mac address.."
    random_mac()
    print "Connecting to Virgin WI-FI.."
    connect_hotspot("VirginTrainsEC-WiFi")

    while True:
        try:
            res = requests.request(method="GET", url=LOGIN_ENDPOINT)
            if res.status_code == 200:
                break
        except Exception:
            print "No connection, waiting.."
            time.sleep(1)

    print "Grabbing free 15 minutes.."

    while not virgin_portal_login():
        print "Selenium is a cry baby :( trying again.."
        time.sleep(0.5)

if __name__ == "__main__":
    while True:
        free_wifi()
        print "Enjoy! Sleeping for 10 minutes.."
        time.sleep(800)
