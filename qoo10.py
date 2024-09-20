import requests
import time
import re
import os
import json
import random
import math
import smtplib
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base import get_setting_value, send_alert
# from base import start_driver, get_setting_value, send_alert
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


status = {}
setting_value = get_setting_value('assets/base.ini')

def send_price_alert(ex_datum, price_after):
    smtp_server = "sv12431.xserver.jp"
    smtp_port = 587
    smtp_username = "info@xs998400.xsrv.jp"
    smtp_password = "bwBtQ9tu2Mq-5v2"

    from_email = "info@xs998400.xsrv.jp"
    to_email = setting_value['alertGmail']
    subject = "価格変動メール"
    title = "Welcome to Our Service"
    body_text = ex_datum['url']
    imageUrl = ex_datum['img_url_main']
    changed_price = str(price_after)

    with open("assets/price_mail.html", "r") as file:
        html_template = file.read()

    html_content = html_template.replace("{{subject}}", subject)
    html_content = html_content.replace("{{title}}", title)
    html_content = html_content.replace("{{imageUrl}}", imageUrl)
    html_content = html_content.replace("{{body}}", body_text)
    html_content = html_content.replace("{{price}}", changed_price)

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

def send_stock_alert(ex_datum):
    smtp_server = "sv12431.xserver.jp"
    smtp_port = 587
    smtp_username = "info@xs998400.xsrv.jp"
    smtp_password = "bwBtQ9tu2Mq-5v2"

    from_email = "info@xs998400.xsrv.jp"
    to_email = setting_value['alertGmail']
    subject = "在庫メール"
    title = "Welcome to Our Service"
    body_text = ex_datum['url']
    imageUrl = ex_datum['img_url_main']

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

def get_api_key():
    api_key_url = f'https://api.qoo10.jp/GMKT.INC.Front.QAPIService/ebayjapan.qapi?key={setting_value['qsmAPIKey']}&v=1.0&returnType=json&method=CertificationAPI.CreateCertificationKey&user_id={setting_value['qsmEmail']}&pwd={setting_value['qsmPassword']}'
    response = requests.get(api_key_url)
    json_response = json.loads(response.text)
    if json_response['ResultMsg'] == "成功":
        api_key = json_response['ResultObject']
        return api_key
    else:
        messagebox.showwarning('失敗', '認証情報が正しくありません。')
        return False
    
def exhibit():
    # with open('assets/temp.dat', 'w') as temp_file:
    #     temp_file.write('0')
    
    # with open('assets/account.ini', 'r') as account_file:
    #     plan = account_file.read()
# __________________________________________ 1.get api key from certification key __________________________________________

    api_key = get_api_key()
    
    if api_key == False:
        return
    
# __________________________________________ 2.read exhibition data and qoo10 category data __________________________________________

    ex_data_path = 'assets/download/amazon_data/amazon_products.json'
    
    with open(ex_data_path, 'r', encoding='utf-8') as json_file:
        ex_data = json.loads(json_file.read())
        
# __________________________________________ 3.create a json file with exhibition data for confirmation __________________________________________
    
    json_path = f'assets/download/qoo10_data/qoo10_products.json'
    with open(json_path, 'r', encoding='utf-8') as json_file:
        qoo10_data = json.loads(json_file.read())
    
# __________________________________________ 4.exhibit (api) __________________________________________
    
    ngWords = setting_value['ngWords'].split(',')
    for ex_datum in ex_data:
    # try:
        print('.................................................................................................')
        with open('assets/temp.dat', 'r', encoding='utf-8') as file:
            contents = file.read()
            rows = contents.split('\n')
        
        for row in rows:
            if '=' in row:
                key, value = row.split('=')
                status[key] = value
        
        if status['qoo'] == '0':
            messagebox.showinfo('OK', '操作が中止されました。')
            return
        
        skip_item = False
        
        if ('|' in ex_datum['title']):
            ItemTitle = ex_datum['title'].split('|')[1][0:99].replace('AliExpress', '')
        else:
            ItemTitle = ex_datum['title'][0:99].replace('AliExpress', '')
        
        for ngw in ngWords:
            if ngw and ngw in ItemTitle:
                print(f'NGWords >>>>>>>>> {ngw} >>>>>>>>>> {ItemTitle}')
                skip_item = True
                break
        
        if skip_item:
            continue
        
        for existing_item in qoo10_data:
            if ItemTitle in existing_item['title'] or ItemTitle == existing_item['title']:
                skip_item = True
                print(">>>>>>>>>>>>>>>>> exhibited <<<<<<<<<<<<<<<<<<")
                break
        
        if skip_item:
            continue
        
        SecondSubCat = ex_datum['category']
        print('SecondSubCat >>>>>>>>>>', SecondSubCat)
        
        random_number = random.randint(1, 100000000)
        SellerCode = f'SKU-{random_number}'
        print('SellerCode >>>>>>>>>>', SellerCode)
        ex_datum['seller_code'] = SellerCode

        ProductionPlace = ex_datum['origin']
        print('ProductionPlace >>>>>>>>>>', ProductionPlace)

        ProductionPlaceType = '2'
        if "日本" in ProductionPlace:
            ProductionPlaceType = '1'
        print('ProductionPlaceType >>>>>>>>>>', ProductionPlaceType)
        
        Weight = ex_datum['weight']
        # Weight = 1.0
        print('Weight >>>>>>>>>>', Weight)
        
        Material = ex_datum['material']
        print('Material >>>>>>>>>>', Material)
        
        StandardImage = ex_datum['img_url_main']
        print('StandardImage >>>>>>>>>>', StandardImage)
        
        image_other_url = ''
        for url in ex_datum['img_url_thumb']:
            image_other_url += url + '$$'
        image_other_url = image_other_url[:-2]
        
        ItemDescription = ex_datum['description']
        ItemPrice = int(ex_datum['price'] * float(setting_value['multiplier']))
        print('ItemPrice >>>>>>>>>>', ItemPrice)
        ex_datum['ali_price'] = ex_datum['price']
        ex_datum['price'] = ItemPrice
        
        ItemQty = ex_datum['quantity']
        print('ItemQty >>>>>>>>>>', ItemQty)
        if not ItemQty == '':
            ItemQty = 1
        
        AvailableDateType = '0'
        print('AvailableDateType >>>>>>>>>>', AvailableDateType)
        
        AvailableDateValue = '1'
        print('AvailableDateValue >>>>>>>>>>', AvailableDateValue)

        try:
            exhibition_url = f"https://api.qoo10.jp/GMKT.INC.Front.QAPIService/Giosis.qapi?key={api_key}&returnType=json&method=ItemsBasic.SetNewGoods&SecondSubCat={SecondSubCat}&OuterSecondSubCat=&Drugtypet=&BrandNo=&ItemTitle={ItemTitle}&PromotionName=&SellerCode={SellerCode}&IndustrialCodeType=&IndustrialCode=&ModelNM=&ManufactureDate=&ProductionPlaceType={ProductionPlaceType}&ProductionPlace={ProductionPlace}&Weight={Weight}&Material={Material}&AdultYN=&ContactInfo=&StandardImage={StandardImage}&image_other_url={image_other_url}&VideoURL=&ItemDescription={ItemDescription}&AdditionalOption=&ItemType=&RetailPrice=&ItemPrice={ItemPrice}&ItemQty={ItemQty}&ExpireDate=&ShippingNo=&AvailableDateType={AvailableDateType}&AvailableDateValue={AvailableDateValue}&Keyword="
            # exhibition_url = f"https://api.qoo10.jp/GMKT.INC.Front.QAPIService/Giosis.qapi?key={api_key}&returnType=json&method=ItemsBasic.SetNewGoods&SecondSubCat={SecondSubCat}&OuterSecondSubCat=&Drugtypet=&BrandNo={BrandNo}&ItemTitle={ItemTitle}&PromotionName=&SellerCode={SellerCode}&IndustrialCodeType=&IndustrialCode=&ModelNM=&ManufactureDate=&ProductionPlaceType={ProductionPlaceType}&ProductionPlace={ProductionPlace}&Weight={Weight}&Material={Material}&AdultYN=&ContactInfo=&StandardImage={StandardImage}&image_other_url={image_other_url}&VideoURL=&ItemDescription={ItemDescription}&AdditionalOption=&ItemType=&RetailPrice=&ItemPrice={ItemPrice}&ItemQty={ItemQty}&ExpireDate=&ShippingNo=&AvailableDateType={AvailableDateType}&AvailableDateValue={AvailableDateValue}&Keyword="

            headers = {}
            payload = {}
            response = requests.request("GET", exhibition_url, headers=headers, data=payload)

            time.sleep(2)
            try:
                ResultMsg = json.loads(response.text)['ResultMsg']
                if ResultMsg == 'SUCCESS':
                    ex_datum['gd_no'] = json.loads(response.text)['ResultObject']['GdNo']
                    ex_datum['status'] = "出品済み"
                    qoo10_data.append(ex_datum)
                    
                    with open(json_path, 'w', encoding='utf-8') as json_file:
                        json.dump(qoo10_data, json_file, ensure_ascii=False, indent=4)
                else:
                    print('出品失敗 >>>>>>>>>>>>>>> 111', response.text)
                    ex_datum['gd_no'] = ''
                    ex_datum['status'] = "未出品"
                    qoo10_data.append(ex_datum)
                    
                    with open(json_path, 'w', encoding='utf-8') as json_file:
                        json.dump(qoo10_data, json_file, ensure_ascii=False, indent=4)
            except:
                print('出品失敗 >>>>>>>>>>>>>>> 2222', response.text)
        except:
            print('出品失敗 >>>>>>>>>>>>>>> 33333', response.text)
        print('.................................................................................................')
    # except:
        # print(">>> There is error data in the item. <<<")
    
    with open('assets/temp.dat', 'w') as temp_file:
        temp_file.write('amazon=0\n')
        temp_file.write('qoo=0')
        
    messagebox.showinfo('OK', "出品完了しました。")


def open_manage_window():
    
    json_path = 'assets/download/qoo10_data/qoo10_products.json'
    with open(json_path, 'r', encoding='utf-8') as file:
        products_info = file.read()
    products = json.loads(products_info)
    
    tbody_content = ''
    for product in products:
        tbody_content += f"""
            <tr class="text-center" id={product['seller_code']}>
                <td>
                    <div class="checkbox">
                        <label><input type="checkbox" value="{product['gd_no']}"></label>
                    </div>
                </td>
                <td>{product['seller_code']}<br/>{product['gd_no']}<br/>{product['status']}</td>
                <td><a href="https:{product['url']}" target="_blank"><p>{product['title']}</p></a></td>
                <td><a href="https:{product['url']}" target="_blank"><img src="{product['img_url_main']}" width="100" height="100" /></a></td>
                <td>{product['price']}円</td>
                <td>{product['quantity']}</td>
            </tr>
            """
            
    manage_screen_content = f"""
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
                            <h3>Qoo10商品情報</h3>
                            <div class="col-md-8">
                            </div>
                            <div class="col-md-4">
                                <input type="search" name="filter" id="filter" class="form-control" placeholder="検索。。。" value="" />
                            </div>
                        </div>

                        <div class="row m-4">
                            <table class="table table-striped table-bordered align-middle">
                                <thead>
                                    <tr class="text-center">
                                        <th><button type="button" class="btn btn-outline-danger btn-sm"  data-bs-toggle="modal" data-bs-target="#myModal">削除</button></th>
                                        <th style="width: 150px;">商品ID</th>
                                        <th style="width: 350px;">商品名</th>
                                        <th>画像</th>
                                        <th>価格</th>
                                        <th>在庫</th>
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
    html_path = 'assets/download/qoo10_data/qoo10_prodcuts.html'
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(manage_screen_content)
    time.sleep(5)
    
    # open html file
    # driver = start_driver()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(os.path.abspath(html_path))
    time.sleep(3)
    
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
        
        delete_items = []
        for chbox in selected_checkboxes:
            if chbox.is_selected():
                delete_items.append(chbox.get_attribute('value'))
                # products = [d for d in products if d.get("gd_no") != chbox.get_attribute('value')]
        
        # with open(json_path, 'w') as json_file:
        #     json.dump(products, json_file, indent=4)      
        # time.sleep(1)
        
        if len(delete_items) == 0:
            messagebox.showwarning('警告', '商品を選択してください。')
            return
        
        setting_value = get_setting_value('assets/base.ini')
        driver.get('https://qsm.qoo10.jp/GMKT.INC.Gsm.Web/Product/ProductListSummary.aspx')
        time.sleep(3)
        
        email_input = driver.find_element(By.NAME, 'txtLoginID')
        email_input.send_keys(setting_value['qsmEmail'])
        pwd_input = driver.find_element(By.NAME, 'txtLoginPwd')
        pwd_input.send_keys(setting_value['qsmPassword'])
        # This is for captcha
        time.sleep(30)
        
        btn_search = driver.find_element(By.ID, 'btn_search')
        btn_search.click()
        time.sleep(3)
        
        total_search_cnt_div = driver.find_element(By.ID, 'div_total_search_cnt')
        total_search_cnt = total_search_cnt_div.find_element(By.CLASS_NAME, 'type_purple').text
        
        product_search_result = driver.find_element(By.CLASS_NAME, 'product_search_result')
        sel_view_data_cnt = product_search_result.find_element(By.ID, 'sel_view_data_cnt')
        options = sel_view_data_cnt.find_elements(By.TAG_NAME, 'option')
        options[len(options) - 1].click()
        time.sleep(3)
        
        total_page_cnt = math.ceil(int(total_search_cnt) / 100)
        
        ex_data_path = f'assets/download/qoo10_data/qoo10_products.json'
        
        while total_page_cnt:
            div_product_list = product_search_result.find_element(By.ID, 'div_product_list')
            products_tr = div_product_list.find_elements(By.TAG_NAME, 'tr')
            
            for item in delete_items:
                for tr in products_tr[1:]:
                    if str(item) in tr.text:
                        tr.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]').click()
                        
                        with open(ex_data_path, 'r', encoding='utf-8') as json_file:
                            ex_data = json.loads(json_file.read())
                            ex_data = [ex_datum for ex_datum in ex_data if ex_datum["gd_no"] != item]
                        
                        with open(ex_data_path, 'w', encoding='utf-8') as json_file:
                            json.dump(ex_data, json_file, indent=4)

            pagination_div = driver.find_element(By.ID, 'search_result_paging_list')
            next_page_btn = pagination_div.find_element(By.ID, 'btn_page_next')
            next_page_btn.click()
            print('clicked')
            time.sleep(5)
            total_page_cnt -= 1
            
        delete_button = product_search_result.find_element(By.XPATH, "//button[text()='商品削除']")
        delete_button.click()
        time.sleep(3)
        
        try:
            alert = driver.switch_to.alert
            alert.accept()

        except NoAlertPresentException:
            print('no confirm alert present')
        
    finally:
        driver.quit()
        

def reexhibit(datum):
    print('reexhibit')


def cancel_exhibit(item):

    # driver = start_driver()
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        setting_value = get_setting_value('assets/base.ini')
        driver.get('https://qsm.qoo10.jp/GMKT.INC.Gsm.Web/Product/ProductListSummary.aspx')
        time.sleep(3)
        
        email_input = driver.find_element(By.NAME, 'txtLoginID')
        email_input.send_keys(setting_value['qsmEmail'])
        pwd_input = driver.find_element(By.NAME, 'txtLoginPwd')
        pwd_input.send_keys(setting_value['qsmPassword'])
        # This is for captcha
        time.sleep(30)
        
        btn_search = driver.find_element(By.ID, 'btn_search')
        btn_search.click()
        time.sleep(3)
        
        product_search_result = driver.find_element(By.CLASS_NAME, 'product_search_result')
        sel_view_data_cnt = product_search_result.find_element(By.ID, 'sel_view_data_cnt')
        options = sel_view_data_cnt.find_elements(By.TAG_NAME, 'option')
        options[len(options) - 1].click()
        time.sleep(3)
        
        div_product_list = product_search_result.find_element(By.ID, 'div_product_list')
        products_tr = div_product_list.find_elements(By.TAG_NAME, 'tr')
        
        for tr in products_tr[1:]:
            if str(item['gd_no']) in tr.text:
                tr.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]').click()
        
        delete_button = product_search_result.find_element(By.XPATH, "//button[text()='商品削除']")
        delete_button.click()
        time.sleep(3)
        
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            print('no 販売中止 confirm alert present')
        
    finally:
        driver.quit()


def checking_price_stock():
    
    # driver = start_driver()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.amazon.co.jp/-/ja/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=jpflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
    time.sleep(3)

    id_bar = driver.find_element(By.ID, 'ap_email')
    id_bar.send_keys(setting_value['amazonEmail'])

    id_button = driver.find_element(By.ID, 'continue')
    id_button.click()

    password_bar = driver.find_element(By.ID, 'ap_password')
    password_bar.send_keys(setting_value['amazonPassword'])

    signin_button = driver.find_element(By.ID, 'signInSubmit')
    signin_button.click()
    time.sleep(2)
    
    ex_data_path = f'assets/download/qoo10_data/qoo10_products.json'
    with open(ex_data_path, 'r', encoding='utf-8') as json_file:
        ex_data = json.loads(json_file.read())
                
    for ex_datum in ex_data:
        
        # with open('assets/temp.dat', 'r') as temp_file:
        #     status = temp_file.read()
        
        # if status == '1':
        #     messagebox.showinfo('OK', '操作が中止されました。')
        #     return
        try:
            driver.get(ex_datum['url'])
            time.sleep(3)
            try:
                price_rate = setting_value['multiplier']
                price_el = driver.find_element(By.CSS_SELECTOR, 'span[class="a-offscreen"]')
                price_text = price_el.get_attribute('innerHTML')
                price_value = int(price_text.replace("￥","").replace(",",""))
                price_rate = float(price_rate)
                price_after = int(round(price_value * price_rate, 2))
                print('>>> price >>>', price_after)
            except NoSuchElementException:
                print(">>> price error >>>")
                continue
            price_before = ex_datum['ali_price']
            if not price_before == price_after:
                print('>>>>>>>>>>>>>>>>>>>> different')
                send_price_alert(ex_datum, price_after)
                time.sleep(3)
                if price_after > price_before:
                    print('....................... big big .....................')
                    cancel_exhibit(ex_datum)
                    time.sleep(3)
                reexhibit(ex_datum)
            try:
                no_isset_quenity_element = driver.find_element(By.ID, "outOfStock")
                out_of_stock_element = no_isset_quenity_element.find_element(By.XPATH, "//span[contains(text(),'現在在庫切れです。')]")
                quantity = out_of_stock_element.text
                print(f"quantity: {no_isset_quenity}")
            except NoSuchElementException:
                no_isset_quenity = None
            print(ex_datum['quantity'], quantity)
            if quantity == '現在在庫切れです。':
                print('stocks runs out')
                send_stock_alert(ex_datum)
                cancel_exhibit(ex_datum)
                
            time.sleep(3)
        except:
            pass


if __name__ == "__main__":
    exhibit()