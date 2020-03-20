#!/bin/env python3

from config import *
# config provides url username and password

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def sleep(sec):
    for x in range(sec):
        print("\rWaiting.." + str(sec - x), end="")
        time.sleep(1)
    print("\r" + " "*40 + "\r", end="")


def initialise_browser():
    option = webdriver.FirefoxOptions()
    option.add_argument("- incognito")

    browser = webdriver.Firefox(executable_path='./geckodriver')
    return browser

def ctfd_scraper(browser)
    browser.get(URL)

    print("Page Loaded ")

    user_field = browser.find_element_by_id("name-input")
    user_field.clear()
    user_field.send_keys(username)

    pass_field = browser.find_element_by_id("password-input")
    pass_field.clear()
    pass_field.send_keys(password)

    submit = browser.find_element_by_xpath("//button[@class='btn btn-md btn-primary btn-outlined float-right']")
    submit.click()


    CTF_challs =[]

    while browser.find_element_by_id('challenges-board').text == "":
        sleep(1)

    challenge_board = browser.find_element_by_id('challenges-board')

    challenge_list = challenge_board.find_elements_by_class_name('pt-5')
    for x in challenge_list:
        category = x.find_element_by_class_name('category-header')
        challenges = x.find_elements_by_class_name('challenge-button')

        for y in challenges:
            y.click()
            while(browser.find_element_by_id('challenge-window').text == ""):
                sleep(1)

            box = browser.find_element_by_class_name('modal-body')
            challenge = box.find_element_by_id('challenge')
            challenge_name = challenge.find_element_by_class_name('challenge-name').text
            challenge_score = challenge.find_element_by_class_name('challenge-value').text
            challenge_desc = challenge.find_element_by_class_name('challenge-desc').text
            try:
                challenge_files = challenge.find_elements_by_class_name('btn-file')
                challenge_files_name = [x.text for x in challenge_files]
                challenge_files_links = [x.get_attribute('href') for x in challenge_files]

            except:
                challenge_files = []

            sleep(1)
            box.find_element_by_class_name('close').click()

            new_chall = {}

            print("Category: " + category.text)
            print("Name: " + challenge_name)
            print("Points: " + challenge_score)
            print("Desc: " + challenge_desc)
            if challenge_files != []:
                print("Files: " + ','.join([x for x in challenge_files_name]))
                print("Links: " + ','.join([x for x in challenge_files_links]))
            print()
            sleep(2)

            new_chall["category"] = category.text
            new_chall["name"] = challenge_name
            new_chall["points"] = challenge_score
            new_chall["desc"] = challenge_desc
            if challenge_files != []:
                new_chall["files"] = ','.join([x for x in challenge_files_name])
                new_chall["links"] = ','.join([x for x in challenge_files_links])

    input("Press any key to quit")
    browser.quit()
    return  CTF_challs
