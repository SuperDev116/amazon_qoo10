# from bs4 import BeautifulSoup
import requests
import time
import re
import pandas as pd
import xlsxwriter
import datetime
import csv
import json

import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.simpledialog import askinteger
from tkinter import *
from tkinter import messagebox

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



with open('qoo10CategoryList.json', encoding='utf-8') as f:
	data = json.load(f)
	categoryData = data['ResultObject']


top = Tk()


def button_clicked():
	current_time = datetime.now()
	target_time = datetime(2024, 2, 15)
	if current_time > target_time:
		print('有効期間切れ')
		return
	
	id_text = text1.get('1.0', tk.END)
	pass_text = text2.get('1.0', tk.END)
	asin_text = text3.get('1.0', tk.END)
	import_text = text4.get('1.0', tk.END)
	price_rate_text = text5.get('1.0', tk.END)
	excluded_asin_text = text6.get('1.0', tk.END)
	excluded_keyword_text = text7.get('1.0', tk.END)
	api_id_text = text8.get('1.0', tk.END)
	api_pass_text = text9.get('1.0', tk.END)
	api_key_text = text10.get('1.0', tk.END)

	if id_text.strip() == "" or pass_text.strip() == "" or asin_text.strip() == "" or api_id_text.strip() == "" or api_pass_text.strip() == "" or api_key_text.strip() == "" :
		if id_text.strip() == "" :
			messagebox.showinfo('警告', 'メールを入力してください')

		if pass_text.strip() == "" :
			messagebox.showinfo('警告', 'パスワードを入力してください')

		if asin_text.strip() == "" :
			messagebox.showinfo('警告', 'ASINと入力してください')

		if api_id_text.strip() == "" :
			messagebox.showinfo('警告', 'ストアIDを入力してください')

		if api_pass_text.strip() == "" :
			messagebox.showinfo('警告', 'パスワードを入力してください')

		if api_key_text.strip() == "" :
			messagebox.showinfo('警告', 'APIキーを入力してください')

	else:
#--------------------------------------------GET API KEY-------------------------------------#
		qoo10_api_url = 'https://api.qoo10.jp/GMKT.INC.Front.QAPIService/Document/QAPIGuideIndex.aspx'
		driver = Chrome()
		driver.get(qoo10_api_url)
		time.sleep(1)

		api_button = driver.find_element(By.XPATH, "//a[contains(text(),'販売認証キー発行')]")
		api_button.click()
		time.sleep(1)

		api_button1 = driver.find_element(By.XPATH, "//a[contains(text(),'CreateCertificationKey')]")
		api_button1.click()
		time.sleep(1)

		api_button3 = driver.find_element(By.XPATH, "//a[contains(text(),'QAPI Test Form')]")
		api_button3.click()
		time.sleep(2)

		certificationKey_bar = driver.find_element(By.ID, 'txt_certificatioin_key')
		certificationKey_bar.send_keys(api_key_text.strip())

		userID_bar = driver.find_element(By.ID, 'txt_param_user_id')
		userID_bar.send_keys(api_id_text.strip())

		paramPWD_bar = driver.find_element(By.ID, 'txt_param_pwd')
		paramPWD_bar.send_keys(api_pass_text.strip())

		send_button = driver.find_element(By.ID, 'btn_method_invoke')
		send_button.click()
		time.sleep(5)

		key_div_tag = driver.find_element(By.ID, 'div_result')
		key_li_tag = key_div_tag.find_element(By.CSS_SELECTOR, '.L1')
		key_span_tag = key_li_tag.find_elements(By.CSS_SELECTOR, '.str')
		key_text = key_span_tag[1].text
		api_key = key_text.replace('"','')
		print("key",api_key)
		driver.close()
#------------------------------------------------------------------------------------------------------#

		base_url = 'https://www.amazon.co.jp/-/ja/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=jpflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'
		product_url = 'https://www.amazon.co.jp/dp/'

		WAIT_SEC = 20

		data = [
			['ASIN', 'インポート名', '出品価格倍率', '除外ASIN', '除外キーワード'],
			[asin_text, import_text, price_rate_text, excluded_asin_text, excluded_keyword_text]
		]

		with open('conditionlist.csv', 'w', newline='' ,encoding='utf-8') as file:
			writer = csv.writer(file)
			writer.writerows(data)

		file.close()

		data_head1 = ['item_number', 'seller_unique_item_id', 'category_number', 'brand_number', 'item_name', 'item_promotion_name', 'item_status_Y/N/D',
			'end_date', 'price_yen', 'retail_price_yen', 'quantity', 'option_info', 'additional_option_info', 'additional_option_text',
			'image_main_url', 'image_other_url', 'video_url', 'image_option_info', 'image_additional_option_info', 'header_html', 'footer_html', 'item_description',
			'Shipping_number', 'option_number', 'available_shipping_date', 'desired_shipping_date', 'search_keyword', 'item_condition_type', 'origin_type', 'origin_region_id', 'origin_country_id', 'origin_others',
			'medication_type', 'item_weight', 'item_material', 'model_name', 'external_product_type', 'external_product_id', 'manufacture_date', 'expiration_date_type', 'expiration_date_MFD', 'expiration_date_PAO',
			'expiration_date_EXP', 'under18s_display_Y/N', 'A/S_info', 'buy_limit_type', 'buy_limit_date', 'buy_limit_qty']

		data_head2 = ['商品番号', '販売者商品コード', 'カテゴリ', 'ブランド', '商品名', '広告文', '販売ステータス',
			'販売終了日', '販売価格', '参考価格', '在庫数量', 'オプション', '追加型オプション(選択)', '追加型オプション(直接入力)',
			'メイン画像', '追加画像', '動画', 'オプションの画像', '追加型オプションの画像', 'ヘッダー', 'フッター', '商品詳細',
			'送料', 'オプション送料', '発送可能日', 'お届け希望日', '検索ワード', '商品状態', '原産地', '原産地_地域名', '原産地_国名', '原産地_その他',
			'医薬品分類', '重量', '素材', 'モデル名', '商品識別コード', '商品識別コード_コード', '製造日', '有効期間', '有効期間_期間1', '有効期間_期間2',
			'有効期間__日付', '18歳未満制限', 'アフターサービス情報', '購入数量制限', '購入数量制限_期間', '購入数量制限_数量']

		workbook = xlsxwriter.Workbook('Qoo10_ItemList.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write_row(0, 0, data_head1)
		worksheet.write_row(1, 0, data_head2)

		def start_driver():
			# Selenium用のウェブドライバーを初期化し、さまざまなオプションで安定した最適なパフォーマンスを得る。
			# Selenium用のChromeドライバーオプションを設定。
			options = webdriver.ChromeOptions()
			options.add_argument('--disable-extensions')  # クリーンなブラウジングセッションのためにブラウザ拡張を無効にする。
			options.add_argument('--start-maximized')  # ブラウザを最大化したウィンドウで開始。参考: https://stackoverflow.com/a/26283818/1689770
			options.add_argument('--no-sandbox')  # 互換性向上のためにサンドボックスを無効にする。参考: https://stackoverflow.com/a/50725918/1689770
			options.add_argument('--disable-dev-shm-usage')  # より安定した動作のためにこのオプションを追加。参考: https://stackoverflow.com/a/50725918/1689770

			# 主処理
			try:
				driver_path = ChromeDriverManager().install()
				service = Service(executable_path=driver_path)
				driver = webdriver.Chrome(service=service, options=options)

			except ValueError:
				# 最新バージョンのChromeドライバーを取得してインストール。
				url = r'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
				response = requests.get(url)
				data_dict = response.json()
				latest_version = data_dict["channels"]["Stable"]["version"]

				driver_path = ChromeDriverManager(version=latest_version).install()
				service = Service(executable_path=driver_path)
				driver = webdriver.Chrome(service=service, options=options)

			except PermissionError:  # 暫定処理 参考: https://note.com/yuu________/n/n14d97c155e5e
				try:
					driver = webdriver.Chrome(service=Service(f'C:\\Users\\{USERNAME}\\.wdm\\drivers\\chromedriver\\win64\\116.0.5845.97\\chromedriver.exe'), options=options)
				except:
					driver = webdriver.Chrome(service=Service(f'C:\\Users\\{USERNAME}\\.wdm\\drivers\\chromedriver\\win64\\116.0.5845.96\\chromedriver.exe'), options=options)

			# ブラウザウィンドウを最大化。
			driver.maximize_window()
			# ウェブドライバの待機時間を設定。
			wait = WebDriverWait(driver, WAIT_SEC)
			return driver


		def main():

			driver = Chrome()
			# driver = start_driver()
			driver.get(base_url)

			id_bar = driver.find_element(By.ID, 'ap_email')
			id_bar.send_keys(id_text.strip())

			id_button = driver.find_element(By.ID, 'continue')
			id_button.click()
			time.sleep(1)

			password_bar = driver.find_element(By.ID, 'ap_password')
			password_bar.send_keys(pass_text.strip())
			time.sleep(1)

			signin_button = driver.find_element(By.ID, 'signInSubmit')
			signin_button.click()
			time.sleep(5)

			onshopping_button = driver.find_elements(By.XPATH, "//button[contains(text(),'ショッピングを続ける')]")
			time.sleep(30)
			if len(onshopping_button)>0:
				messagebox.showinfo('警告', 'キャプチャを解除してツールを再起動してください')
				driver.close()
				time.sleep(20)
			else:
				save_index = 1
				lines = asin_text.splitlines()
				import_file_name = text4.get('1.0', tk.END)

				for line in lines:
					# if line in exclusion_text:
					if line in excluded_asin_text.split('\n'):
						continue
					else:
						driver.get(product_url + line)
						time.sleep(5)
						print(line)
	#------------------------------------------------------  ItmQty  ----------------------------------------------------------#
						try:
							qty_sel = driver.find_elements(By.ID, 'quantity')
							if len(qty_sel)>0:
								qty_sel = driver.find_element(By.ID, 'quantity')
								qty_options = qty_sel.find_elements(By.TAG_NAME, "option")
								ItemQty = len(qty_options)
							else :
								ItemQty = 0
						except NoSuchElementException:
							print("except:")
						time.sleep(3)
	#-------------------------------------------Product category----------------------------------------------------#
						try:
							category_a1_text = ""
							category_a2_text = ""
							category_a3_text = ""
							category_qoo_code = ""
							category_ul = driver.find_element(By.CSS_SELECTOR, ".a-unordered-list.a-horizontal.a-size-small")
							category_a = category_ul.find_elements(By.TAG_NAME, "a")
							category_a1 = category_a[0].text
							if category_a1 == "" or ItemQty == 0:
								continue
							else :
								quantity = int(ItemQty)
								category_a1_text = category_a1.strip()
								category_a2 = category_a[1].text
								category_a2_text = category_a2.strip()
								category_a3 = category_a[2].text
								category_a3_text = category_a3.strip()

								print("category_a1_text:" + category_a1_text)
								print("category_a2_text:" + category_a2_text)
								print("category_a3_text:" + category_a3_text)

								# df = pd.read_excel('categorymatchingsheet.xlsx')

								# amazon_subcategory = df['amazon_subcategory']
								# amazon_category = df['amazon_category']
								# qoo_matchingcode = df['qoo_matchingcode']

								# for index, am_cat in enumerate(amazon_subcategory):
								#     am_cat = str(am_cat)
								#     if category_a2_text in am_cat:
								#         category_qoo_code = qoo_matchingcode[index]

								# if  category_qoo_code == "":
								#     for index, bm_cat in enumerate(amazon_category):
								#         if category_a1_text in bm_cat:
								#            category_qoo_code = qoo_matchingcode[index]
								#
								# category_qoo_code = "300000001"

								for category in categoryData:
									if category_a3_text in category['CATE_S_NM'] or category['CATE_S_NM'] in category_a3_text:
										category_qoo_code = category['CATE_S_CD']
										break

									if category_a2_text in category['CATE_M_NM'] or category['CATE_M_NM'] in category_a2_text:
										category_qoo_code = category['CATE_M_CD']
										break

									if category_a1_text in category['CATE_L_NM'] or category['CATE_L_NM'] in category_a1_text:
										category_qoo_code = category['CATE_L_CD']
										break

								print('Qoo10 category code', category_qoo_code)
								print('quantity', str(quantity))
								time.sleep(2)

	#-------------------------------------------item name----------------------------------------------#
								try:
									item_name =""
									item_text = driver.find_element(By.ID, 'productTitle').text
									keywords_text = text7.get('1.0', tk.END)
									keywords = keywords_text.splitlines()
									for keyword in keywords:
										if keyword in item_text:
											item_name = item_text.replace(keyword, "")
									print("item_name:" + item_name)

									medication_type = ''
									if '医薬品' in category_a2_text:
										if '第1類医薬品' in item_text:
											medication_type = '1C'
										elif '第2類医薬品' in item_text:
											medication_type = '2C'
										elif '第3類医薬品' in item_text:
											medication_type = '3C'
										elif '指定第2類医薬品' in item_text:
											medication_type = 'D2'
										elif '医薬部外品' in item_text:
											medication_type = 'QD'
										else :
											medication_type = ''
									print("medication_type:" + medication_type)
								except NoSuchElementException:
									print("item_name:")
								time.sleep(1)
	#-------------------------------------------item_status-------------------------------------------------------#
								item_status = "Y"
								print("item_status:" + item_status)
	#-------------------------------------------end_date-------------------------------------------------------#
								end_date = "2023-12-31"
								print("end_date:" + end_date)
								time.sleep(1)

	#-------------------------------------------image_main_url-----------------------------------------------------#
								img_ul = driver.find_element(By.CSS_SELECTOR, ".a-unordered-list.a-nostyle.a-horizontal.list.maintain-height")
								image_main_li = img_ul.find_element(By.XPATH, "//li[@data-csa-c-posy = '1']")
								image_main_tag = image_main_li.find_element(By.TAG_NAME, 'img')
								image_main_url = image_main_tag.get_attribute('src')
								print("image_main_url:" + image_main_url)
								time.sleep(1)
	#-------------------------------------------image_other_url-----------------------------------------------------#
								image_li = driver.find_elements(By.CSS_SELECTOR, "li.imageThumbnail")
								image_li_count = len(image_li)
								image_other = ""
								for x in range(image_li_count):
									image_other_li = driver.find_element(By.XPATH, f"//li[@data-csa-c-posy='{x+1}']")
									image_other_tag = image_other_li.find_element(By.TAG_NAME, 'img')
									image_other_src = image_other_tag.get_attribute('src')
									image_other += image_other_src + "$$"
								image_other_url = image_other[:-2]
								print("image_other_url:" + image_other_url)
								time.sleep(1)
	#-----------------------------------------------Product Description-----------------------------------------------------#
								item_description = ""
								description_div = driver.find_elements(By.ID, 'productDescription_feature_div')
								if len(description_div)>0:
									description_div = driver.find_element(By.ID, 'productDescription_feature_div')
									item_description = description_div.text.strip()
									if item_description == "":
										item_description = "商品の説明"
									try:
										a_note = description_div.find_element(By.TAG_NAME, 'a')
										text_note = a_note.text
										item_description = item_description.replace(text_note, "")
									except NoSuchElementException:
										print("except")
								else :
									item_description = "商品の説明"
								print("description:" + item_description)
	#-------------------------------------------Shipping_number-------------------------------------------------------#
								shipping_number = int(0)
								print(shipping_number)
	#----------------------------------------------available_shipping_date-------------------------------------------#

								try:
									purchase_delivery_text = ""
									availableDateType = ""
									availableDateValue =""
									delivery_month = ""
									purchase_delivery_div = driver.find_elements(By.ID, "oneTimePurchaseDefaultDeliveryDate")
									delivery_div = driver.find_elements(By.ID, "mir-layout-DELIVERY_BLOCK")
									if  len(purchase_delivery_div)>0:
										purchase_delivery_text = driver.find_element(By.ID, "oneTimePurchaseDefaultDeliveryDate").text
										purchase_delivery_month = purchase_delivery_text.split("月")[0]
										purchase_delivery_day = purchase_delivery_text.split("月")[1]
										def get_numbers(purchase_delivery_month):
											pattern = r"\d+"
											return re.findall(pattern, purchase_delivery_month)
										purchase_delivery_month =  get_numbers(purchase_delivery_month)
										purchase_delivery_month = str([int(x) for x in purchase_delivery_month])
										purchase_delivery_month = purchase_delivery_month.replace("[","").replace("]","")
										purchase_delivery_day =  get_numbers(purchase_delivery_day)
										purchase_delivery_day = str([int(x) for x in purchase_delivery_day])
										purchase_delivery_day = purchase_delivery_day.replace("[","").replace("]","")
										today = datetime.datetime.now()
										year = today.year
										if today.month > int(purchase_delivery_month):
											year = int(year) + 1
										target_date = str(year) + "/" + purchase_delivery_month + "/" + purchase_delivery_day
										availableDateType =  "2"
										availableDateValue = target_date
										print(availableDateType, availableDateValue)
									elif len(delivery_div)>0:
										delivery_div = driver.find_element(By.ID, "mir-layout-DELIVERY_BLOCK")
										delivery_span1 = delivery_div.find_elements(By.XPATH, "//span[contains(text(),'月')]")
										delivery_span2 = delivery_div.find_elements(By.XPATH, "//span[contains(text(),'本日中')]")
										if len(delivery_span2)>0 :
											availableDateType =  "0"
											availableDateValue = "1"
										elif len(delivery_span1)>0:
											delivery_text_div = delivery_div.find_element(By.XPATH, "//span[contains(text(),'月')]")
											delivery_text = delivery_text_div.text
											delivery_text_len = delivery_text.split("月")
											delivery_month = delivery_text_len[0]
											if len(delivery_text_len)>1:
												delivery_day = delivery_text.split("月")[1]
												if "-" in delivery_day:
													delivery_day = delivery_day.split("-")[0]
											def get_numbers(delivery_month):
												pattern = r"\d+"
												return re.findall(pattern, delivery_month)
											if  get_numbers(delivery_month):
												delivery_month =  get_numbers(delivery_month)
											delivery_month = str([int(x) for x in delivery_month])
											delivery_month = delivery_month.replace("[","").replace("]","")
											delivery_day =  get_numbers(delivery_day)
											delivery_day = str([int(x) for x in delivery_day])
											delivery_day = delivery_day.replace("[","").replace("]","")
											today = datetime.datetime.now()
											year = today.year
											if today.month > int(delivery_month):
												year = int(year) + 1
											target_date = (datetime.datetime(year, int(delivery_month), int(delivery_day)) - today).days
											target_date = target_date + 1
											if target_date>3:
												availableDateType =  "1"
											else :
												availableDateType =  "0"
											availableDateValue = str(target_date)

									print(availableDateType, availableDateValue)

								except NoSuchElementException:
									print("except")

								time.sleep(1)

	#----------------------------------------------item_condition_type-------------------------------------------#

								item_condition_type = int(1)
								print(item_condition_type)
								time.sleep(1)
	#----------------------------------------------origin_type--------------------------------------------------#
								try:
									origin_name = ""
									origin_type = ""
									origin_code = ""
									ccode = ""
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
										origin_name = origin

									elif len(origin_th)>0:
										origin_th = driver.find_element(By.XPATH, "//th[contains(text(),'原産国')]")
										td_text = origin_th.find_element(By.XPATH, "./following-sibling::td").text
										origin_name = td_text.strip()
									else:
										origin_type = int(1)
										origin_name = "日本"
									if "日本" in origin_name:
										origin_type = int(1)
									elif origin_name == "":
										origin_type = int(1)
										origin_name = "日本"
									else:
										origin_type = int(2)
										df = pd.read_excel('countrycodelist.xlsx')
										country_list = df['Country Name']
										country_code_list = df['Country Code']
										for index, am_cat in enumerate(country_list):
											if am_cat in origin_name:
												origin_code = country_code_list[index]
									print(origin_name)
									print(origin_type)
									print("origin_code:"+origin_code)
								except NoSuchElementException:
									print('exception')
								time.sleep(1)
	#-------------------------------------------Product brand-------------------------------------------------------#
								try:
									brand_no = ""
									brand_code = ""
									brand_tr = driver.find_element(By.CSS_SELECTOR, ".a-spacing-small.po-brand")
									brand_td = brand_tr.find_element(By.CSS_SELECTOR, ".a-span9")
									brand_no = brand_td.text.strip()
									print(brand_no)
									df = pd.read_csv('BrandList.csv')
									brand_list = df['Japanese']
									brand_code_list = df['Brand No.']
									for index, am_cat in enumerate(brand_list):
										if am_cat == brand_no:
											brand_code = brand_code_list[index]
									print(brand_code)
								except NoSuchElementException:
									print("except")
								time.sleep(1)

	#-------------------------------------------Packing size and weight-----------------------------------------------------#
								try:
									item_weight = ""
									productDetails_table=driver.find_element(By.ID, 'productDetails_techSpec_section_1')
									th_tags = productDetails_table.find_elements(By.TAG_NAME, "th")
									for th_tag in th_tags:
										if "梱包サイズ" or "製品サイズ" in th_tag.text:
											td_text = th_tag.find_element(By.XPATH, "./following-sibling::td").text
											if ";" in td_text:
												td_details = td_text.split(";")
												packing_weight = td_details[1].strip()

												if 'kg' in packing_weight:
													item_weight = packing_weight.replace("kg", "").strip()
													item_weight = float(item_weight)
												else :
													packing_weight = packing_weight.replace("g", "").strip()
													if '.' in packing_weight:
														packing_weight = packing_weight.split('.')[0]
														packing_weight = int(packing_weight)
													else :
														packing_weight = int(packing_weight)
													item_weight = round(packing_weight / 1000, 2)
													item_weight = float(item_weight)
												print(item_weight)
											else :
												packing_size = td_text
								except NoSuchElementException:
									print('exception')
								time.sleep(1)
	#------------------------------------------------------  Material   ---------------------------------------------------#
								try:
									material_text = ""
									material_el = driver.find_elements(By.CSS_SELECTOR, ".po-material_feature")
									if len(material_el)>0:
										material_el = driver.find_element(By.CSS_SELECTOR, ".po-material_feature")
										material_span = material_el.find_elements(By.TAG_NAME, 'span')
										item_material = material_span[1].text.strip()
									else :
										item_material = ""
									print("item_material",item_material)
								except NoSuchElementException:
									print('exception')
	#-------------------------------------------price_yen-------------------------------------------------------#
								try:
									price_rate = text5.get('1.0', tk.END)
									price_el = driver.find_element(By.CSS_SELECTOR, 'span[class="a-offscreen"]')
									price_text = price_el.get_attribute('innerHTML')
									price_value = int(price_text.replace("￥","").replace(",",""))
									price_rate = float(price_rate)
									# price_yen = round(price_value * price_rate)
									price_yen = int(round(price_value * price_rate, 2))

									print(price_yen)
								except NoSuchElementException:
									print("except")
								time.sleep(1)

	#-----------------------------------------------------------------------------------------------------------------#
								data = [
									save_index,
									'',
									category_qoo_code,
									brand_code,
									item_name,
									'',
									item_status,
									end_date,
									price_yen,
									'',
									quantity,
									'',
									'',
									'',
									image_main_url,
									image_other_url,
									'',
									'',
									'',
									'',
									'',
									item_description,
									''
									'',
									availableDateValue,
									'',
									'',
									item_condition_type,
									origin_type,
									'',
									origin_code,
									'',
									medication_type,
									item_weight,
									item_material,
									'',
									'',
									'',
									'',
									'',
									'',
									'',
									'',
									'',
									'',
									'',
									'',
									'',
								]
								save_index = save_index +1
								worksheet.write_row(save_index, 0, data)
								url = f"https://api.qoo10.jp/GMKT.INC.Front.QAPIService/Giosis.qapi?key={api_key}&returnType=json&method=ItemsBasic.SetNewGoods&SecondSubCat={category_qoo_code}&OuterSecondSubCat=&Drugtypet={medication_type}&BrandNo={brand_code}&ItemTitle={item_name}&PromotionName=&SellerCode=&IndustrialCodeType=&IndustrialCode=&ModelNM=&ManufactureDate=&ProductionPlaceType={origin_type}&ProductionPlace={origin_name}&Weight={item_weight}&Material={item_material}&AdultYN=&ContactInfo=&StandardImage={image_main_url}&VideoURL=&ItemDescription={item_description}&AdditionalOption=&ItemType=&RetailPrice=&ItemPrice={price_yen}&ItemQty={quantity}&ExpireDate=&ShippingNo=&AvailableDateType={availableDateType}&AvailableDateValue={availableDateValue}&Keyword="

								payload = {}
								headers = {}
								print(url)
								response = requests.request("GET", url, headers=headers, data=payload)

								print(response.text)

						except NoSuchElementException:
							print("except:")

				workbook.close()

				driver.close()

		if __name__ == '__main__':
			main()
#------------------------------------------------Interface----------------------------------------------------#
top.geometry("400x670")
top.title("条件登録")

custom_font = font.Font(size=12)
style = ttk.Style()
style.configure('TLabel', foreground='red')

file = open("registerdata.txt", "r")
file_contents = file.read()
file.close()
lines = file_contents.splitlines()
mail_text = lines[0].strip()
pass1_text = lines[1].strip()
id_text = lines[2].strip()
pass2_text = lines[3].strip()
api_text = lines[4].strip()

custom_font = font.Font(size=8)
var1 = StringVar()
Labal1 = Label( top, textvariable=var1, relief=RAISED, font = custom_font)
var1.set("Eメールまたは携帯電話番号")
Labal1.place(x=50, y=15)

text1 = Text(top)
text1.insert(END, mail_text)
text1.place(x=50, y=40, width=300, height=25)

var2 = StringVar()
Labal2 = Label( top, textvariable=var2, relief=RAISED)
var2.set("パスワード")
Labal2.place(x=50, y=70)

text2 = Text(top)
text2.insert(END, pass1_text)
text2.place(x=140, y=70, width=210, height=25)

var3 = StringVar()
Labal3 = ttk.Label( top, textvariable=var3, relief=RAISED)
var3.set("ASIN入力")
Labal3.place(x=50, y=100)

text3 = Text(top)
text3.place(x=50, y=125, width=120, height=120)

var4 = StringVar()
Labal4 = Label( top, textvariable=var4, relief=RAISED )
var4.set("インポート名")
Labal4.place(x=180, y=100)

text4 = Text(top)
text4.place(x=180, y=125, width=170, height=120)

var5 = StringVar()
Labal5 = Label( top, textvariable=var5, relief=RAISED)
var5.set("出品価格倍率")
Labal5.place(x=50, y=250)

text5 = Text(top)
text5.insert(END, "1.2")
text5.place(x=140, y=250, width=210, height=25)

var6 = StringVar()
Labal6 = Label( top, textvariable=var6, relief=RAISED)
var6.set("除外ASIN入力")
Labal6.place(x=50, y=280)

text6 = Text(top)
text6.place(x=50, y=305, width=300, height=100)

var7 = StringVar()
Labal7 = Label( top, textvariable=var7, relief=RAISED)
var7.set("除外キーワード入力")
Labal7.place(x=50, y=410)

text7 = Text(top)
text7.place(x=50, y=435, width=300, height=70)

var8 = StringVar()
Labal8 = Label( top, textvariable=var8, relief=RAISED)
var8.set("ストアID")
Labal8.place(x=50, y=510)

text8 = Text(top)
text8.insert(END, id_text)
text8.place(x=140, y=510, width=210, height=21)

var9 = StringVar()
Labal9 = Label( top, textvariable=var9, relief=RAISED)
var9.set("パスワード")
Labal9.place(x=50, y=536)

text9 = Text(top)
text9.insert(END, pass2_text)
text9.place(x=140, y=536, width=210, height=21)

var10 = StringVar()
Labal10 = Label( top, textvariable=var10, relief=RAISED )
var10.set("APIキー")
Labal10.place(x=50, y=562)

text10 = Text(top)
text10.insert(END, api_text)
# text10.config(state='disabled')
text10.place(x=110, y=562, width=240, height=68)

style = ttk.Style()
style.configure('TButton', background='blue')

B = ttk.Button(top, text ="登録", command=button_clicked)
B.place(x=250,y=635, width=100)

top.mainloop()
#---------------------------------------------------------------------------------------------------------------#
