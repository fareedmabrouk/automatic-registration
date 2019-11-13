
from collections import defaultdict
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import getpass

#Instantiate chrome webdriver
driverpath = "C:\\Users\\Malik\\Desktop\\Automatic Class Scheduler\\chromedriver.exe"

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
def login():
        elem = driver.find_element_by_id("weblogin_netid")
        elem.send_keys(username)
        elem = driver.find_element_by_id("weblogin_password")
        elem.send_keys(password)
        driver.find_element_by_id('submit_button').click()
def get_spots(sln):
    if (check_exists_by_xpath("//td[normalize-space()='" + sln + "']//following-sibling::th")):
        return int(driver.find_element_by_xpath("//td[normalize-space()='" + sln + "']//following-sibling::th").text)
    else:
        print("Can't find SLN code on page!")
        return 0
def sign_up_both(lecture, quiz):
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")
    element = driver.find_elements_by_id("submit_button")
    if element:
        login()
    if drop_list:
        drop_lectures()
    driver.find_element_by_name("sln7").send_keys(lecture)
    driver.find_element_by_name("sln8").send_keys(quiz)
    driver.find_element_by_xpath('//*[@id="regform"]/input[7]').click()

def sign_up(lecture):
    driver.get("https://sdb.admin.uw.edu/students/uwnetid/register.asp")
    element = driver.find_elements_by_id("submit_button")
    if element:
        login()
    if drop_list:
        drop_lectures()
    driver.find_element_by_name("sln7").send_keys(lecture)
    driver.find_element_by_xpath('//*[@id="regform"]/input[7]').click()

def check_lectures():
    for curr_lecture in lecture_quiz:
        if lecture_quiz[curr_lecture]:
            for curr_quiz in lecture_quiz[curr_lecture]:
                if get_spots(curr_quiz) > 0:
                    sign_up_both(curr_lecture, curr_quiz)
                    print("Found an open spot! I signed you up for lecture " + curr_lecture + " and quiz section " + curr_quiz)
                    return True
        elif not lecture_quiz[curr_lecture]:
            if get_spots(curr_lecture) > 0:
                sign_up(curr_lecture)
                print("Found an open spot! I signed you up for lecture " + curr_lecture)
                return True
    return False
def page_exists():
    driver.get("https://sdb.admin.uw.edu/timeschd/uwnetid/tsstat.asp?QTRYR=WIN+2020&CURRIC=" + department)
    time.sleep(3)
    element = driver.find_elements_by_id("submit_button")
    if element:
        login()
    time.sleep(2)
    if not driver.current_url.startswith("https://sdb.admin.uw.edu/timeschd/uwnetid/tsstat.asp?QTRYR="):
        print("Registration is currently unavailable, trying again soon.")
        return False
    return True
def drop_lectures():
    for sln in drop_list:
        driver.find_element_by_xpath('//tt[contains(text(), \'' + sln + '\')]//ancestor::td/preceding-sibling::td').click()
username = input('Enter your NetID: ')
password = getpass.getpass('Enter your password: ')

department = input('What is the department code?: ').upper()
num_lectures = int(input('How many lectures codes?: '))



lecture_quiz = defaultdict(list)
counter = 0
while counter < num_lectures:
    counter = counter + 1
    lecture_quiz[input("Enter lecture code: ")] = []
for entry in lecture_quiz:
    num_quizzes = int(input('How many quiz codes for lecture ' + entry + '?: '))
    counter2 = 0;
    while counter2 < num_quizzes:
        temp_quiz = input('Enter quiz code: ')
        counter2 = counter2 + 1
        lecture_quiz[entry].append(temp_quiz)
has_drop = False
drop_list = []
num_drops = int(input('How many SLNs to drop?: '))
counter = 0
while(counter < num_drops):
    drop_list.append(input('Enter SLN drop: '))
    counter += 1
print(drop_list)

#OPEN SPRING 2020 TIME SCHEDULE PAGE
driver = webdriver.Chrome(driverpath)
driver.get("https://sdb.admin.uw.edu/timeschd/uwnetid/tsstat.asp?QTRYR=WIN+2020&CURRIC=" + department)
login()
found_course = False
attempt = 0;
while not found_course:
    time.sleep(43)
    d = datetime.datetime.now()
    curr_time = round((d.hour + d.minute / 60. + d.second / 3600.), 2)
    if curr_time > 10:
        print("Current time value is : " + str(curr_time))
        attempt = attempt + 1
        print("Attempt #" + str(attempt))
        print(datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S"))
        if page_exists():
            if check_lectures():
                found_course = True
            else:
                print("All spots taken, checking again in 50 seconds.")
        else:
            attempt -= 1
    else:
        print("The time is not right... checking again soon.")
        print(curr_time)
print("You have been signed up for your desired class!")
