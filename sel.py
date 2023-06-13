# create an api endpoint
# </bestseller> to scrape smartphone prices from best-seller list amazon.com
# and return data in json format.
# </smartphone> to scrape smartphone name,price,user-rating

from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/smartphone')
def smartphone():
    driver = webdriver.Firefox()
    driver.get('https://www.amazon.in/')
    driver.maximize_window()
    link = driver.find_element_by_link_text("Best Sellers")
    link.click()
    driver.find_element_by_link_text("See More").click()
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    box_element = driver.find_elements(By.CLASS_NAME, '_cDEzb_grid-column_2hIsc')
    json_dic = []
    for i in box_element:
        try:
            name_element = i.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
            price_element = i.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-price_3mJ9Z')
            rating = i.find_element(By.CSS_SELECTOR, ".a-icon-alt").get_attribute("innerHTML")
            price = price_element.text
            new_dic = {}
            new_dic['product_name'] = name_element.text
            new_dic['product_price'] = str(price.split('₹')[-1]) + '  Rs' 
            new_dic['product_rating'] = rating
            json_dic.append(new_dic)
        except:
            pass
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'a-pagination').find_element_by_link_text("2").click()
    time.sleep(2)
    box_element = driver.find_elements(By.CLASS_NAME, '_cDEzb_grid-column_2hIsc')
    for i in box_element:
        try:
            name_element = i.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
            price_element = i.find_element(By.CLASS_NAME, '_cDEzb_p13n-sc-price_3mJ9Z')
            rating = i.find_element(By.CSS_SELECTOR, ".a-icon-alt").get_attribute("innerHTML")
            new_dic = {}
            new_dic['product_name'] = name_element.text
            new_dic['product_price'] = price_element.text
            new_dic['product_rating'] = rating
            json_dic.append(new_dic)
        except:
            pass
    driver.quit()
    return jsonify({"data" : json_dic}) #name,price,user-rating i

@app.route('/bestseller')
def bestseller():
    driver = webdriver.Firefox()
    driver.get('https://www.amazon.in/gp/bestsellers/electronics/1389432031/ref=zg_bs_nav_electronics_2_3561110031')
    driver.maximize_window()
    prices = driver.find_elements(By.CLASS_NAME, '_cDEzb_p13n-sc-price_3mJ9Z')
    price_list= []
    for i in prices:
        try:
            price = i.text
            price_list.append(str(price.split('₹')[-1]) + '  Rs')
        except:
            pass
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'a-pagination').find_element_by_link_text("2").click()
    time.sleep(2)
    prices = driver.find_elements(By.CLASS_NAME, '_cDEzb_p13n-sc-price_3mJ9Z')
    for i in prices:
        try:
            price = i.text
            price_list.append(str(price.split('₹')[-1]) + '  Rs')
        except:
            pass
    driver.quit()
    return jsonify({"data" : price_list})

if __name__ == '__main__':
    app.run(debug=True)