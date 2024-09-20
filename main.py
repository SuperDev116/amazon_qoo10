import tkinter as tk
import threading
from datetime import datetime
from tkinter import messagebox
from base import open_setting_window
from amazon import scraping, open_checking_window
from qoo10 import exhibit, checking_price_stock, open_manage_window


status = {}

def run_open_setting_window_in_thread():
    threading.Thread(target=open_setting_window).start()
    
def run_scraping_in_thread():
    with open('assets/temp.dat', 'r', encoding='utf-8') as file:
        contents = file.read()
        rows = contents.split('\n')
    
    for row in rows:
        if '=' in row:
            key, value = row.split('=')
            status[key] = value

    if status['qoo'] == '1':
        messagebox.showwarning('警告', '現在Qoo10に商品を出品しています。')
        return
    
    if status['amazon'] == '0':
        with open('assets/temp.dat', 'w') as temp_file:
            temp_file.write('amazon=1\n')
            temp_file.write(f'qoo={status["qoo"]}')

        threading.Thread(target=scraping).start()
    else:
        messagebox.showwarning('警告', '現在Amazonから商品データをスクレイピングしています。')
        return
    
def run_open_checking_window_in_thread():
    threading.Thread(target=open_checking_window).start()
    
def run_exhibit_in_thread():
    with open('assets/temp.dat', 'r', encoding='utf-8') as file:
        contents = file.read()
        rows = contents.split('\n')
    
    for row in rows:
        if '=' in row:
            key, value = row.split('=')
            status[key] = value

    if status['amazon'] == '1':
        messagebox.showwarning('警告', '現在Amazonから商品データをスクレイピングしています。')
        return
    
    if status['qoo'] == '0':
        with open('assets/temp.dat', 'w') as temp_file:
            temp_file.write(f'amazon={status["amazon"]}\n')
            temp_file.write('qoo=1')

        threading.Thread(target=exhibit).start()
    else:
        messagebox.showwarning('警告', '現在Qoo10に商品を出品しています。')
        return
    
def run_open_manage_window_in_thread():
    threading.Thread(target=open_manage_window).start()

def run_checking_price_stock_in_thread():
    threading.Thread(target=checking_price_stock).start()
    

def stop_operation():

    with open('assets/temp.dat', 'w') as temp_file:
        temp_file.write('amazon=0\n')
        temp_file.write('qoo=0')
    
    
def draw_main_window():
    
    with open('assets/temp.dat', 'w') as temp_file:
        temp_file.write('amazon=0\n')
        temp_file.write('qoo=0')

    setting_window = tk.Tk()
    setting_window.title('出品ツールAmazonQ10')
    setting_window.geometry('750x500')

    lbl_title = tk.Label(
        text='ダッシュボード',
        font=('Arial', 24)
    )
    lbl_title.pack()
    lbl_title.place(x=250, y=50)

    # 出品情報設定
    btn_win_bid = tk.Button(
        setting_window,
        text='出品設定',
        command=run_open_setting_window_in_thread,
        font=('Arial', 14),
        width=15,
        height=3,
        bg='#808000',
        fg='white'
    )
    btn_win_bid.pack()
    btn_win_bid.place(x=100, y=150)

    # アリエクスクレイピング
    btn_combined_sale = tk.Button(
        setting_window,
        text='AMAZON\nスクレイピング',
        command=run_scraping_in_thread,
        font=('Arial', 14),
        width=15,
        height=3,
        bg='#808000',
        fg='white'
    )
    btn_combined_sale.pack()
    btn_combined_sale.place(x=300, y=150)

    # スクレイピングデータ確認
    btn_combined_sale = tk.Button(
        setting_window,
        text='スクレイピング\nデータ確認',
        command=run_open_checking_window_in_thread,
        font=('Arial', 14),
        width=15,
        height=3,
        bg='#808000',
        fg='white'
    )
    btn_combined_sale.pack()
    btn_combined_sale.place(x=500, y=150)
    
    # Qoo10出品
    btn_exhibit = tk.Button(
        setting_window,
        text='Qoo10出品',
        command=run_exhibit_in_thread,
        font=('Arial', 14),
        width=15,
        height=3,
        bg='#808000',
        fg='white',
    )
    btn_exhibit.pack()
    btn_exhibit.place(x=100, y=250)

    # 商品管理画面
    btn_cancel_listing = tk.Button(
        setting_window,
        text='Qoo10商品管理',
        command=run_open_manage_window_in_thread,
        font=('Arial', 14),
        width=15,
        height=3,
        bg='#808000',
        fg='white',
    )
    btn_cancel_listing.pack()
    btn_cancel_listing.place(x=300, y=250)
    
    # 価格在庫確認
    btn_scraping = tk.Button(
        setting_window,
        text='価格在庫確認',
        command=run_checking_price_stock_in_thread,
        font=('Arial', 14),
        width=15,
        height=3,
        bg='#808000',
        fg='white',
    )
    btn_scraping.pack()
    btn_scraping.place(x=500, y=250)
    
    # 中止ボタン
    btn_cancel_listing = tk.Button(
        setting_window,
        text='操作中止',
        command=stop_operation,
        font=('Arial', 14),
        width=15,
        height=3,
        bg='#808000',
        fg='white',
    )
    btn_cancel_listing.pack()
    btn_cancel_listing.place(x=300, y=350)
    
    setting_window.mainloop()
    
    
if __name__ == '__main__':
    
    specific_date = datetime(2024, 9, 30)
    current_date = datetime.now()

    if specific_date < current_date:
        print('>>> expired <<<')
    else:
        draw_main_window()