import time
import re
import os
import json
import smtplib
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from base import get_setting_value
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


status = {}
BASE_URL = 'https://www.amazon.co.jp/-/ja/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=jpflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'
PRODUCT_URL = 'https://www.amazon.co.jp/dp/'
def send_email_alert(main_image, productUrl, alertGmail):
	smtp_server = "sv12431.xserver.jp"
	smtp_port = 587
	smtp_username = "info@xs998400.xsrv.jp"
	smtp_password = "bwBtQ9tu2Mq-5v2"

	from_email = "info@xs998400.xsrv.jp"
	to_email = alertGmail
	subject = "在庫確認メール"
	title = "Welcome to Our Service"
	body_text = productUrl
	imageUrl = main_image

	with open("assets/mail.html", "r") as file:
		html_template = file.read()

	html_content = html_template.replace("{{subject}}", subject)
	html_content = html_content.replace("{{title}}", title)
	html_content = html_content.replace("{{imageUrl}}", imageUrl)
	html_content = html_content.replace("{{body}}", body_text)


	msg = MIMEMultipart("alternative")
	msg["From"] = from_email
	msg["To"] = to_email
	msg["Subject"] = subject

	msg.attach(MIMEText(html_content, "html"))

	try:
		server = smtplib.SMTP(smtp_server, smtp_port)
		server.set_debuglevel(1)
		server.starttls()

		server.login(smtp_username, smtp_password)

		server.sendmail(from_email, to_email, msg.as_string())

		server.quit()
		print("Email sent successfully.")
	except Exception as e:
		print(f"Error: {e}")


def read_category_data():
    try:
        with open("assets/qc_dict.json", "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("qc_dict.json file not found. Please save the category data first.")
        return {}
    return data


def find_category_code(dictionary, search_key):
    for key, value in dictionary.items():
        if key == search_key:
            return value
        elif isinstance(value, dict):
            category_code = find_category_code(value, search_key)
            if category_code is not None:
                return category_code
    return None


def scraping():

    setting_value = get_setting_value('assets/base.ini')
    
    products_info = []
    json_path = 'assets/download/amazon_data/amazon_products.json'
    with open(json_path, 'r', encoding='utf-8') as json_file:
        products_info = json.load(json_file)
    
    json_path = f'assets/download/amazon_data/amazon_products.json'
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(BASE_URL)

    id_bar = driver.find_element(By.ID, 'ap_email')
    id_bar.send_keys(setting_value['amazonEmail'])

    id_button = driver.find_element(By.ID, 'continue')
    id_button.click()

    password_bar = driver.find_element(By.ID, 'ap_password')
    password_bar.send_keys(setting_value['amazonPassword'])

    signin_button = driver.find_element(By.ID, 'signInSubmit')
    signin_button.click()
    time.sleep(30)

    exhiAsins = setting_value['exhiAsins'].split(',')
    ngAsins = setting_value['ngAsins'].split(',')
    ngWords = setting_value['ngWords']
    multiplier = setting_value['multiplier']
    category = setting_value['qoo_smallCategory']
    alertGmail = setting_value['alertGmail']

    index = 1
    for asin in exhiAsins:
        if asin in ngAsins:
            continue
        # try:
        with open('assets/temp.dat', 'r', encoding='utf-8') as file:
            contents = file.read()
            rows = contents.split('\n')
        
        for row in rows:
            if '=' in row:
                key, value = row.split('=')
                status[key] = value
        
        if status['amazon'] == '0':
            messagebox.showinfo('OK', '操作が中止されました。')
            return
        
        driver.get(PRODUCT_URL + asin)
        time.sleep(3)
        try:
            Noasin_element = driver.find_element(By.XPATH, "//b[contains(text(), '何かお探しですか？')]")
            no_asin = Noasin_element.text
        except NoSuchElementException:
            no_asin = None

        # try:
        #     prime_element = driver.find_element(By.XPATH, "//div[@id='ppd']")
        #     image_elements = prime_element.find_elements(By.TAG_NAME, "img")
        #     for img in image_elements:
        #         if_prime = img.get_attribute("src")
        #         if if_prime == "https://m.media-amazon.com/images/G/09/perc/prime-logo.svg":
        #             return if_prime
        # except NoSuchElementException:
        try:
            prime_element = driver.find_element(By.XPATH, "//div[@id='shippingMessageInsideBuyBox_feature_div']")
            if_prime = prime_element.find_element(By.CSS_SELECTOR, ".a-icon.a-icon-prime")
            print(f"-----------------------------------------%%%%%%%------>>>>>>>>>>>>>>>>>>{if_prime}")
        except NoSuchElementException:
            try:
                prime_element = driver.find_element(By.XPATH, "//div[@id='shippingMessageInsideBuyBox_feature_div']")
                if_prime = prime_element.find_element(By.CSS_SELECTOR, ".a-icon.a-icon-prime.tabs")
                print(f"-----------------------------------------%%%%%%%------>>>>>>>>>>>>>>>>>>{if_prime}")
            except NoSuchElementException:
                if_prime = None

        if not no_asin == "何かお探しですか？":
            print(f"-------------------end----------------------%%%%%%%------>>>>>>>>>>>>>>>>>>{if_prime}")
            if if_prime != None:

                product_info = {}

                product_info['url'] = PRODUCT_URL + asin
                print('>>> url >>>', product_info['url'])

        #-----------================no isset quenity
                try:
                    no_isset_quenity_element = driver.find_element(By.ID, "outOfStock")
                    out_of_stock_element = no_isset_quenity_element.find_element(By.XPATH, "//span[contains(text(),'現在在庫切れです。')]")
                    no_isset_quenity = out_of_stock_element.text
                    print(f"no_isset_quenity: {no_isset_quenity}")
                except NoSuchElementException:
                    no_isset_quenity = None
        #---------------------------no isset quenity end

        #---------------------------free delivery
                try:
                    delivery_div = driver.find_element(By.ID, "mir-layout-DELIVERY_BLOCK")
                    free_delivery_ = delivery_div.find_elements(By.XPATH, "//span[contains(text(),'無料配送')]")
                    free_delivery = len(free_delivery_)
                except NoSuchElementException:
                    free_delivery = 0
                print(f">>> free_delivery >>>> {free_delivery}")
        #----------------------------free delivery end
                
        #----------------------------quantity
                try:
                    qty_sel = driver.find_element(By.ID, 'quantity')
                    qty_options = qty_sel.find_elements(By.TAG_NAME, "option")
                    product_info['quantity'] = len(qty_options)
                except NoSuchElementException:
                    product_info['quantity'] = 1
                print('>>> quantity information >>>', product_info['quantity'])
        #-----------------------------quantity end
                
        #-----------------------------product name            
                item_text = driver.find_element(By.ID, 'productTitle').text
                keywords_text = ngWords
                keywords = keywords_text.split(",")

                for keyword in keywords:
                    if keyword in item_text:
                        product_info['title'] = item_text.replace(keyword, "")
                    else:
                        product_info['title'] = item_text
                print('>>> title >>>', product_info['title'])
        #-----------------------------product name end 

        #-----------------------------main image url
                img_ul = driver.find_element(By.CSS_SELECTOR, ".a-unordered-list.a-nostyle.a-horizontal.list.maintain-height")
                # image_main_li = img_ul.find_element(By.XPATH, "//li[@data-csa-c-posy = '1']")
                image_main_li = img_ul.find_element(By.ID, "imgTagWrapperId")
                image_main_tag = image_main_li.find_element(By.TAG_NAME, 'img')
                product_info['img_url_main'] = image_main_tag.get_attribute('src')
                # product_info['img_url_main'] = image_main.replace("US40", "SL875")
                print('>>> main image url >>>', product_info['img_url_main'])
        #-----------------------------main image url end

        #-----------------------------thumb image url
                image_li = driver.find_elements(By.CSS_SELECTOR, "li.imageThumbnail")
                image_li_count = len(image_li)
                image_other = []

                for x in range(image_li_count):
                    image_other_li = driver.find_element(By.XPATH, f"//li[@data-csa-c-posy='{x+1}']")
                    image_other_tag = image_other_li.find_element(By.TAG_NAME, 'img')
                    image_other_src = image_other_tag.get_attribute('src').replace("US40", "SL875")
                    image_other.append(image_other_src)

                product_info['img_url_thumb'] = image_other
                print('>>> thumb image url >>>', product_info['img_url_thumb'])
        #-----------------------------thumb image url end

        #-----------------------------price
                try:
                    price_rate = multiplier
                    price_el = driver.find_element(By.CSS_SELECTOR, 'span[class="a-offscreen"]')
                    price_text = price_el.get_attribute('innerHTML')
                    price_value = int(price_text.replace("￥","").replace(",",""))
                    price_rate = float(price_rate)
                    # price_yen = round(price_value * price_rate)
                    product_info['price'] = int(round(price_value, 2))
                    print('>>> price >>>', product_info['price'])
                except NoSuchElementException:
                    print(">>> price error >>>")
                    continue
        #-----------------------------price end 

        #-----------------------------category
                category_json_data = read_category_data()
                product_info['category'] = find_category_code(category_json_data, category)
                print('>>> category >>>', product_info['category'])
        #-----------------------------category end 
        
        #-----------------------------description
                try:
                    description_div = driver.find_element(By.ID, 'productDescription_feature_div')
                    product_info['description'] = description_div.text.strip()
                    if product_info['description'] == "":
                        product_info['description'] = "商品の説明"
                    try:
                        a_note = description_div.find_element(By.TAG_NAME, 'a')
                        text_note = a_note.text
                        product_info['description'] = product_info['description'].replace(text_note, "")
                    except NoSuchElementException:
                        pass
                    print('>>> description >>>', product_info['description'])
                except NoSuchElementException:
                    product_info['description'] = "商品の説明"
                    print('>>> description >>>', product_info['description'])
        #-----------------------------description end
        
        #-----------------------------origin
                try:
                    product_info['origin'] = ""
                    origin_type = ""
                    origin_code = ""
                    origin_el = driver.find_elements(By.XPATH, "//span[contains(text(),'原産国')]")
                    origin_th = driver.find_elements(By.XPATH, "//th[contains(text(),'原産国')]")
                    if len(origin_el)>0:
                        origin_el = driver.find_element(By.XPATH, "//span[contains(text(),'原産国')]")
                        if ':' in origin_el.text:
                            origin = origin_el.text.split(':')[1].strip()
                            if origin == '':
                                next_span = origin_el.find_element(By.XPATH, "following-sibling::span[1]")
                                origin = next_span.text.strip()
                        elif '：' in origin_el.text:
                            origin = origin_el.text.split('：')[1].strip()
                        elif '】' in origin_el.text:
                            origin = origin_el.text.split('】')[1].strip()
                        else:
                            ancestor_th_el = origin_el.find_element(
                                By.XPATH, './ancestor::th[1]')
                            next_td = ancestor_th_el.find_element(
                                By.XPATH, "following-sibling::td[1]")
                            origin = next_td.text
                        product_info['origin'] = origin

                    elif len(origin_th)>0:
                        origin_th = driver.find_element(By.XPATH, "//th[contains(text(),'原産国')]")
                        td_text = origin_th.find_element(By.XPATH, "./following-sibling::td").text
                        product_info['origin'] = td_text.strip()
                    else:
                        origin_type = int(1)
                        product_info['origin'] = "日本"
                    if "日本" in product_info['origin']:
                        origin_type = int(1)
                    elif product_info['origin'] == "":
                        origin_type = int(1)
                        product_info['origin'] = "日本"

                    print('>>> origin >>>', product_info['origin'])
                except NoSuchElementException:
                    product_info['origin'] = ""  
                    print('>>> origin >>>', product_info['origin'])       
        #-----------------------------origin end

        #-----------------------------weight     
                try:
                    product_info['weight'] = ""
                    productDetails_table=driver.find_element(By.ID, 'productDetails_techSpec_section_1')
                    th_tags = productDetails_table.find_elements(By.TAG_NAME, "th")
                    for th_tag in th_tags:
                        if "梱包サイズ" or "製品サイズ" in th_tag.text:
                            td_text = th_tag.find_element(By.XPATH, "./following-sibling::td").text
                            if ";" in td_text:
                                td_details = td_text.split(";")
                                packing_weight = td_details[1].strip()

                                if 'kg' in packing_weight:
                                    product_info['weight'] = packing_weight.replace("kg", "").strip()
                                    product_info['weight'] = float(product_info['weight'])
                                else :
                                    packing_weight = packing_weight.replace("g", "").strip()
                                    if '.' in packing_weight:
                                        packing_weight = packing_weight.split('.')[0]
                                        packing_weight = int(packing_weight)
                                    else :
                                        packing_weight = int(packing_weight)
                                    product_info['weight'] = round(packing_weight / 1000, 2)
                                    product_info['weight'] = float(product_info['weight'])
                                print('>>> weight >>>', product_info['weight'])
                            else :
                                packing_size = td_text
                except NoSuchElementException:
                    product_info['weight'] = ""
                    print('>>> weight >>>', product_info['weight'])
        #-----------------------------weight end

        #-----------------------------material
                try:
                    material_el = driver.find_element(By.CSS_SELECTOR, ".po-material_feature")
                    material_span = material_el.find_elements(By.TAG_NAME, 'span')
                    product_info['material'] = material_span[1].text.strip()
                    print('>>> material >>>', product_info['material'])
                except NoSuchElementException:
                    product_info['material'] = ""
                    print('>>> material >>>', product_info['material'])
        #-----------------------------material end
                
                product_info['exhibit'] = 1
                product_info['reason'] = ''
                product_info['id'] = index
                index += 1
                
                time.sleep(3)
                if no_isset_quenity == "現在在庫切れです。":
                    productUrl = product_info['url']
                    send_email_alert(product_info['img_url_main'], productUrl, alertGmail)
                    continue
                if free_delivery != 0:
                    products_info.append(product_info)
                    with open(json_path, 'w', encoding='utf-8') as json_file:
                        json.dump(products_info, json_file, ensure_ascii=False, indent=4)
                else:
                    continue 
            else:
                continue
        else:
            continue
        # except:
        #     pass
    driver.quit()
    
    with open('assets/temp.dat', 'w') as temp_file:
        temp_file.write('amazon=0\n')
        temp_file.write('qoo=0')
        
    messagebox.showinfo("OK", "スクレイピング完了しました。")


def open_checking_window():
    
    json_path = 'assets/download/amazon_data/amazon_products.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        products_info = file.read()
    products = json.loads(products_info)
    
    tbody_content = ''
    for product in products:
        tbody_content += f"""
            <tr class="text-center">
                <td>
                    <div class="checkbox">
                        <label><input type="checkbox" value="{product['id']}"></label>
                    </div>
                </td>
                <td><a href="https:{product['url']}" target="_blank"><p>{product['title']}</p></a></td>
                <td><a href="https:{product['url']}" target="_blank"><img src="{product['img_url_main']}" width="100" height="100" /></a></td>
                <td>{product['price']}</td>
                <td>{product['quantity']}</td>
            </tr>
            """
            
    html_content = f"""
    <!DOCTYPE html>
    <html>

    <head>
        <!-- Latest compiled and minified CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

        <!-- Latest compiled JavaScript -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    </head>

    <body>

        <div class="container">
            <form id="information_form">
                <div class="row">
                    <div class="col-md-12">
                        <div class="row m-4">
                            <h3>amazon商品情報（価格と在庫を確認しましょう！）</h3>
                            <div class="col-md-8">
                            </div>
                            <div class="col-md-4">
                                <input type="search" name="filter" id="filter" class="form-control" placeholder="検索。。。" value="" />
                            </div>
                        </div>

                        <div class="row m-4">
                            <table class="table table-striped table-bordered amazongn-middle">
                                <thead>
                                    <tr class="text-center">
                                        <th><button type="button" class="btn btn-outline-danger btn-sm"  data-bs-toggle="modal" data-bs-target="#myModal">削除</button></th>
                                        <th style="width: 500px;">商品名</th>
                                        <th style="width: 200px;">画像</th>
                                        <th style="width: 200px;">価格</th>
                                        <th style="width: 300px;">在庫</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {tbody_content}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </form>
        </div>
        
        <div class="modal" id="myModal">
            <div class="modal-dialog">
                <div class="modal-content">

                    <!-- Modal Header -->
                    <div class="modal-header">
                        <h4 class="modal-title">警告</h4>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>

                    <!-- Modal body -->
                    <div class="modal-body">
                        選択された商品を本当に削除しますか？
                    </div>

                    <!-- Modal footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" onclick="return alert('商品を削除します。少々お待ちください。')">確認</button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">キャンセル</button>
                    </div>

                </div>
            </div>
        </div>
        
        <script>
            $(document).ready(function(){{
                $('#filter').on('input', function() {{
                    var keyword = $(this).val().toLowerCase();
                    $('tbody tr').filter(function() {{
                        $(this).toggle($(this).text().toLowerCase().indexOf(keyword) > -1);
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    # generate html file
    html_path = 'assets/download/amazon_data/amazon_prodcuts.html'
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    time.sleep(5)
    
    # driver = start_driver()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(f"file:///{os.path.abspath(html_path)}")
    
    try:
        WebDriverWait(driver, 600).until(
            EC.alert_is_present()
        )
        
        time.sleep(3)
        
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            print('no confirm alert present')
        
        selected_checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        
        for chbox in selected_checkboxes:
            if chbox.is_selected():
                id = chbox.get_attribute('value')
                
                with open(json_path, 'r', encoding='utf-8') as json_file:
                    amazon_data = json.loads(json_file.read())
                    amazon_data = [amazon_datum for amazon_datum in amazon_data if str(amazon_datum["id"]) != id]
                    
                with open(json_path, 'w', encoding='utf-8') as json_file:
                    json.dump(amazon_data, json_file, indent=4)
            
    finally:
        driver.quit()
        
                
if __name__ == '__main__':
    # scraping()
    open_checking_window()
    