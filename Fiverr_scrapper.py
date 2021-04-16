import time

import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.by import By

link1 = "https://www.fiverr.com/search/gigs?query=guest%20post&source=top-bar&acmpl=1&search_in=everywhere&search" \
        "-autocomplete-original-term=&search-autocomplete-available=true&search-autocomplete-type=recent-gigs-suggest" \
        "&search-autocomplete-position=0&page=1"

links = []
source = []
des = []
ds = []
wb = xlsxwriter.Workbook("Data.xlsx")

sheet1 = wb.add_worksheet('Sheet-1')
sheet1.set_column(0, 2, 50)
sheet1.write(0, 0, "Links")
sheet1.write(0, 1, "Source")
sheet1.write(0, 2, "description")


def page_number():
    num1 = 10
    num = 1
    it = 1
    while True:
        driver1 = webdriver.Chrome()
        url = "https://www.fiverr.com/search/gigs?query=guest%20post&source=top-bar&acmpl=1&search_in=everywhere&search" \
              "-autocomplete-original-term=&search-autocomplete-available=true&search-autocomplete-type=recent-gigs" \
              "-suggest" \
              "&search-autocomplete-position=0&page=" + str(num) + ""
        driver1.get(url)
        html_list = driver1.find_element_by_id("pagination")
        items = html_list.find_elements_by_tag_name("li")
        text = ''
        text2 = ''
        for item in items:
            text2 = text
            text = item.text
        num = int(text2)
        print(num)
        driver1.quit()
        if num < num1 * it:
            break
        it = it + 1
    return num


def readd(file, colum):
    val = 1
    with open(file, "r") as f:
        for line in f:
            sheet1.write(val, colum, line)
            val = val + 1


def read2():
    vl = 1
    for lk in ds:
        sheet1.write(vl, 2, lk)
        vl = vl + 1


def xml_write():
    readd("bin/links.txt", 0)
    readd("bin/source.txt", 1)
    read2()
    wb.close()


def write_txt(file_name, array):
    with open(file_name, "w") as f1:
        for line in array:
            f1.write(line + "\n")
        f1.close()


def desc(arra):
    for str1 in arra:
        str1 = str1.partition("?context")[0]
        str1 = (str1.rpartition("/")[2].replace("-", " "))
        str1 = "I will do " + str1
        des.append(str1)
    write_txt("bin/description.txt", des)


def dis():
    ln = []
    with open("bin/links.txt", "r") as f3:
        for line in f3:
            ln.append(line)
        for ll in ln:
            driver = webdriver.Chrome()
            driver.get(ll)
            txt = driver.find_element(By.XPATH, "//div[@id=\'perseus-app\']/div/div[3]/div/div[2]").text
            driver.quit()
            time.sleep(1)
            ds.append(txt)
        desc(ds)


def scrap(num):
    k = 0
    i = 0
    # page_num = page_number()
    try:
        driver = webdriver.Chrome()
        url = "https://www.fiverr.com/search/gigs?query=guest%20post&source=pagination&acmpl=1&search_in=everywhere" \
              "&search-autocomplete-original-term=&search-autocomplete-available=true&search-autocomplete-type" \
              "=recent" \
              "-gigs-suggest&search-autocomplete-position=0&page=" + str(num) + "&offset=-2 "
        driver.get(url)
        elems = (driver.find_elements_by_xpath("//a[@href]"))
        for elem in elems:
            i = i + 1
            if 38 < i < 231:
                if elem.get_attribute("href") not in links:
                    k = k + 1
                    if k > 1 and ("?source=gig_card" not in elem.get_attribute("href")):
                        links.append(elem.get_attribute("href"))
                    if "?source=gig_card" in elem.get_attribute("href"):
                        source.append(elem.get_attribute("href"))
        elems.clear()
        driver.quit()
    except ValueError:
        print("Some Error Happened")


pgn = int(input("Page number to scrape:"))

scrap(pgn)
write_txt("bin/source.txt", source)
write_txt("bin/links.txt", links)
dis()

xml_write()
# desc(links)
