from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import time

# Credentials and settings
LOGIN = input("Facebook email: ")
PASSWORD = getpass("Facebook password: ")
MIN_OF_MUTUAL_FRIENDS = int(input("Amount of mutual friends (min): "))
FRIEND_ACCOUNT_LINK = input(
    "Link to your friend's account where his/her friends are listed: ")

# Config
option = Options()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--enable-extensions")
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1  # Allow notifications
})

PATH = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(chrome_options=option, executable_path=PATH)

driver.get("https://www.facebook.com")

# Accept facebook cookies popup
ACCEPT_COOKIE_BTN_XPATH = '//*[@id="u_0_h"]'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, ACCEPT_COOKIE_BTN_XPATH))).click()

# Log in
email_input = driver.find_element_by_id("email")
password_input = driver.find_element_by_id("pass")
login_submit = driver.find_element_by_xpath('//*[@id="u_0_b"]')

email_input.send_keys(LOGIN)
password_input.send_keys(PASSWORD)
login_submit.click()

time.sleep(2)

# Go to friend's profile
driver.get(FRIEND_ACCOUNT_LINK)

# Add friends
FRIEND_TILE_CLASS = '.bp9cbjyn.ue3kfks5.pw54ja7n.uo3d90p7.l82x9zwi.n1f8r23x.rq0escxv.j83agx80.bi6gxh9e.discj3wi.hv4rvrfc.ihqw7lf3.dati1w0a.gfomwglr'
ADD_BUTTON_CLASS = '.oajrlxb2.s1i5eluu.gcieejh5.bn081pho.humdl8nn.izx4hr6d.rq0escxv.nhd2j8a9.j83agx80.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.d1544ag0.qt6c0cv9.tw6a2znq.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l.beltcj47.p86d2i9g.aot14ch1.kzx2olss.cbu4d94t.taijpn5t.ni8dbmo4.stjgntxs.k4urcfbm.tv7at329'
friend_index = 0

while True:
    friends = driver.find_elements_by_css_selector(FRIEND_TILE_CLASS)

    for friend in friends[friend_index:]:
        try:
            can_add_friend = friend.text.split("\n")[2] == "Dodaj"
            mutual_count = int(friend.text.split("\n")[1].split(" ")[0])
            friend_name = friend.text.split("\n")[0]
            friend_index += 1

            # Check for pop-up (security)
            try:
                if driver.find_element_by_xpath('//*[@id="facebook"]/body/div[4]/div[1]/div/div[2]/div/div/div/div[4]/div'):
                    time.sleep(2)
                    driver.find_element_by_xpath(
                        '//*[@id="facebook"]/body/div[4]/div[1]/div/div[2]/div/div/div/div[4]/div').click()
            except:
                pass

            if mutual_count >= MIN_OF_MUTUAL_FRIENDS and can_add_friend:
                add_friend_btn = friend.find_element_by_css_selector(
                    ADD_BUTTON_CLASS)
                add_friend_btn.click()
                print(
                    f"Invite was sent to: {friend_name} | You have {mutual_count} mutual friends")
            else:
                continue
        except:
            continue

    # Scroll down to the bottom to load more friends
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
