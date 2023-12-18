from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import accountInfoGenerator as account
import getVerifCode as verifiCode
from selenium import webdriver
import fakeMail as email
from time import sleep
import argparse
# import parse



parse = argparse.ArgumentParser()

args = parse.parse_args()
ua = UserAgent()
userAgent = ua.random
print(userAgent)


#replace 'your path here' with your chrome binary absolute path
driver = webdriver.Chrome(r'chromedriver.exe')

#saves the login & pass into accounts.txt file.
acc = open("accounts.txt", "a")

driver.get("https://www.instagram.com/accounts/emailsignup/")
sleep(8)
try:
    cookie = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                         '/html/body/div[3]/div/div/button[1]'))).click()
except:
	pass
name = account.username()

#Fill the email value
email_field = driver.find_element_by_name('emailOrPhone')
fake_email = email.getFakeMail()
email_field.send_keys(fake_email)
print(fake_email)

# Fill the fullname value
fullname_field = driver.find_element_by_name('fullName')
fullname_field.send_keys(account.generatingName())
print(account.generatingName())

# Fill username value
username_field = driver.find_element_by_name('username')
username_field.send_keys(name)
print(name)

# Fill password value
password_field = driver.find_element_by_name('password')
acc_password = account.generatePassword()
password_field.send_keys(acc_password) # You can determine another password here.

print(name+":"+acc_password, file=acc)

acc.close()
WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form[class='_aah-'] div div[class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1e56ztr x540dpk x1m39q7l x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']"))).click()

sleep(8)

#Birthday verification
sleep(4)
driver.find_element_by_xpath("//select[@title='Ay:']").click()
sleep(1)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//option[@title='Mart']"))).click()

driver.find_element_by_xpath("//select[@title='Gün:']").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//option[@title='3']"))).click()

driver.find_element_by_xpath("//select[@title='Yıl:']").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//option[@title='2000']"))).click()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1sxyh0.xurb0ha.x1l90r2v.xyamay9.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1"))).click()
sleep(3)
#
fMail = fake_email[0].split("@")
mailName = fMail[0]
domain = fMail[1]
instCode = verifiCode.getInstVeriCode(mailName, domain, driver)
driver.find_element_by_name('email_confirmation_code').send_keys(instCode, Keys.ENTER)
sleep(10)

#accepting the notifications.
driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
sleep(2)

#logout
driver.find_element_by_xpath(
    "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img").click()
driver.find_element_by_xpath(
    "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[2]/div").click()

try:
    not_valid = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div')
    if(not_valid.text == 'That code isn\'t valid. You can request a new one.'):
      sleep(1)
      driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[1]/div[2]/div/button').click()
      sleep(10)
      instCodeNew = verifiCode.getInstVeriCodeDouble(mailName, domain, driver, instCode)
      confInput = driver.find_element_by_name('email_confirmation_code')
      confInput.send_keys(Keys.CONTROL + "a")
      confInput.send_keys(Keys.DELETE)
      confInput.send_keys(instCodeNew, Keys.ENTER)
except:
      pass

sleep(5)

################# to mention 2 persons
post_url = "https://www.instagram.com/p/Cz9RLwDMsw6/"
driver.get(post_url)
sleep(5) 

# Locate the comment box and post a comment
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Add a comment…']"))
    )
    comment_box = driver.find_element_by_css_selector("textarea[aria-label='Add a comment…']")
    comment = "@maxime1602021 @maxime103729283 🍀 "  # Modify the comment text as needed
    comment_box.send_keys(comment)

    post_button = driver.find_element_by_xpath("//button[text()='Post']")
    post_button.click()
except Exception as e:
    print("Error while trying to post a comment:", e)

############### to follow michou
# Navigate to the specific user's Instagram profile
user_profile_url = "https://www.instagram.com/michou/"
driver.get(user_profile_url)
sleep(5)  # Wait for the page to load

# Click the 'Follow' button
try:
    follow_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Follow']"))
    )
    follow_button.click()
except Exception as e:
    print("Error while trying to follow the user:", e)


#######like the post 



# Navigate to the specific Instagram post
post_url = "https://www.instagram.com/p/Cz9RLwDMsw6/"
driver.get(post_url)
sleep(5)  # Wait for the page to load

# Click the 'Like' button
try:
    # The heart icon for liking a post can be identified by its aria-label attribute
    like_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Like']"))
    )
    like_button.click()
except Exception as e:
    print("Error while trying to like the post:", e)


##### 

driver.quit() #logout
