from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

more_pages = True

#############################################################################


def next_page():
    """moves to next page"""
    global more_pages, driver, job_links
    time.sleep(2)
    current_page = int(driver.find_element(By.CSS_SELECTOR, '.artdeco-pagination__indicator.active.selected').text)
    pages = driver.find_elements(By.CSS_SELECTOR, '.artdeco-pagination__indicator')
    total_pages = int(pages[len(pages) - 1].text)
    print(f"current page is {current_page}, total pages is {total_pages}")
    if total_pages == current_page:
        more_pages = False
    else:
        pages[current_page].click()
        time.sleep(5)


def job_list_adder(last_item):
    """adds urls of each post to a list"""
    global job_links
    jobs = driver.find_elements(By.CSS_SELECTOR, '.job-card-container__link.job-card-list__title')
    total_jobs = len(jobs)
    print(f"{total_jobs} total jobs in this list")
    element = jobs[total_jobs - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    for i in jobs:
        link = i.get_attribute("href")
        if link not in job_links:
            job_links.append(link)
            print(len(job_links))
    if last_item == job_links[-1]:
        next_page()
        print("next page")


def find_all_jobs():
    """continues using above two functions"""
    global driver, more_pages, job_links
    while more_pages:
        try:
            last_item = job_links[-1]
        except IndexError:
            last_item = None

        # job_links = job_list_adder()
        job_list_adder(last_item)


def submit_application():
    """get name of button"""
    global driver, havent_applied
    button = driver.find_element(By.CSS_SELECTOR, "button.jobs-apply-button") #clicks first button
    button.click()
    application_button = driver.find_element(By.CSS_SELECTOR, "button.artdeco-button.artdeco-button--2.artdeco-button--primary")
    ########fix to this after
    # application_button.click()
    # button_text = application_button.text
    # if button_text == "Submit application":
    #     return

    button_text = application_button.text
    if button_text == "Submit application":
        dismiss = driver.find_element(By.CSS_SELECTOR, "button.artdeco-modal__dismiss")
        dismiss.click()
        save = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[3]/button[2]")
        time.sleep(1)
        save.click()
        print("would have been submitted but instead saved")

    else:
        dismiss = driver.find_element(By.CSS_SELECTOR, "button.artdeco-modal__dismiss")
        dismiss.click()
        save = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[3]/button[2]")
        time.sleep(1)
        save.click()
        time.sleep(3)
        print("saved because multiple steps")
    havent_applied = False


def check_if_applied():
    global driver, havent_applied, total_jobs
    page = driver.find_elements(By.CSS_SELECTOR, ".mt5")
    for i in page:
        if i.text == "":
            print("already applied")
            total_jobs -= 1
            havent_applied = False

#########################
#see how long program takes to apply to x jobs (x determined later)
start_time = time.time()
##############################################################################################
# pulls up URL which has set parameters already

LINK = "https://www.linkedin.com/jobs/search/?distance=100&f_AL=true&f_JT=F&f_WT=" \
       "1%2C2%2C3&geoId=101140016&keywords=biomedical%20engineer&location=Williston%20Park%2C%" \
       "20New%20York%2C%20United%20States"

ser = Service(r"C:\Users\Sean\Development\chromedriver.exe")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

###################################################
# logging in

USERNAME = os.getenv('EMAIL_17')
PASSWORD = os.getenv('LINKEDIN_PASSWORD')

driver.get(LINK)
time.sleep(2)

login_button = driver.find_element(By.XPATH, '/html/body/div[1]/header/nav/div/a[2]')
login_button.click()
time.sleep(2)

username = driver.find_element(By.XPATH, '//*[@id="username"]')
username.send_keys(f"{USERNAME}{Keys.TAB}{PASSWORD}{Keys.ENTER}")
time.sleep(7)

################
#create list with urls for every job

job_links = []
find_all_jobs()
total_jobs = len(job_links)
for i in range(total_jobs):
    print(i)
    driver.get(job_links[i])
    time.sleep(2)

####################################
    #check to make sure application has not already been submitted:

    havent_applied = True
    check_if_applied()
    while havent_applied:

#######################################
    # submitting application: saves applications with multiple steps

        submit_application()

######################################

print(f"It took {time.time() - start_time} seconds to save {total_jobs}")
print((time.time() - start_time)/total_jobs)

