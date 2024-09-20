import requests
import json
import tkinter as tk
from tkinter import messagebox
from main import draw_main_window


def submit_login():
        
    tool_id = tool_id_entry.get()
    tool_pass = tool_pass_entry.get()
    
    if tool_id == '':
        print("ツールIDは必須です。")
        messagebox.showwarning("警告", "ツールIDは必須です。")
        return
    if tool_pass == '':
        print("ツールPASSは必須です。")
        messagebox.showwarning("警告", "ツールPASSは必須です。")
        return
    
    # Make a request to the server API
    # login_api_url = f'https://xs998400.xsrv.jp/api/v1/login_check'
    login_api_url = f'https://qoo10manageable.info/api/v1/login_check'
    payload = {'tool_id': tool_id, 'tool_pass': tool_pass, 'platform': 'amazon'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(login_api_url, headers=headers, data=payload)
    decoded_data = json.loads(response.text)
        
    # Handle the API response
    if decoded_data['status'] == 200:
        print("200, ログインサクセス")

        login_window.destroy()
        draw_main_window()
        return True
    
    elif decoded_data['status'] == 403:
        print("403, 無効なツールIDです。")
        messagebox.showwarning("警告", "無効なツールIDです。")
        return False
    elif decoded_data['status'] == 401:
        print("401, 無効なツールIDです。")
        messagebox.showwarning("警告", "無効なツールPASSです。")
        return False
    elif decoded_data['status'] == 419:
        print("419, 無効なツールIDです。")
        messagebox.showwarning("警告", "有効期間切れです。")
        return False


# Create the main window
login_window = tk.Tk()
login_window.title("ログイン")
login_window.geometry('200x150')

# ToolID input
tool_id_label = tk.Label(login_window, text="ツールID :")
tool_id_label.pack()
tool_id_label.place(x=20, y=30)
tool_id_entry = tk.Entry(login_window)
tool_id_entry.pack()
tool_id_entry.place(x=90, y=30, width=90)

# ToolPASS input
tool_pass_label = tk.Label(login_window, text="ツールPASS :")
tool_pass_label.pack()
tool_pass_label.place(x=20, y=60)
tool_pass_entry = tk.Entry(login_window, show="*")
tool_pass_entry.pack()
tool_pass_entry.place(x=90, y=60, width=90)

# Submit button
submit_button = tk.Button(login_window, text="ログイン", command=submit_login)
submit_button.pack()
submit_button.place(x=80, y=100)

# Start the Tkinter main loop
login_window.mainloop()
