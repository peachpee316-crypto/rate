"""為替レート計算アプリ(スクレイピング)"""

import tkinter as tk,tkinter.ttk as ttk
import datetime as dt
import requests
from bs4 import BeautifulSoup

# ----------GUI--------------------------------

root = tk.Tk()
root.title("リアルタイム為替レート計算アプリ")
root.minsize(700,400)
root["bg"] = "#e5ffcc"  #薄い黄色


#------webスクレイピング--------
res = requests.get("https://www.smbc.co.jp/ex/ExchangeServlet?ScreenID=real")
res.encoding = res.apparent_encoding      #文字化け対応
# print(res.status_code)  #200
# print(res.text[:500])  #OK

#解析できる型に変更
kekka = BeautifulSoup(res.text,"html.parser")

#tdタグの中身をすべて取得、リストに変更
temp = list(kekka.find_all("td")) 
# print(temp)
#3つ1組が為替1通貨の情報 [0]米ドル（1 USD） 買い値[1]146.97 売値[2]147.97 [3]ユーロ（1 EUR）[4]171.09 [5]172.49

# リストを3つづつの二次元配列に
temp2=[]
for i in range(0,len(temp),3): 
    temp2.append(temp[i:i+3])
    #print(temp2)

def get_rate_dic():
     rate_dic = {}
     for val in temp2:
          rate_dic[val[0].text] = float(val[2].text)
     return rate_dic

rate_dic = get_rate_dic()
print(rate_dic)

#--------------レート計算----------------
def late_ex():
     error["text"] = "" #初めにtextのエラーメッセージを空に設定。※見えてないエラー対応テキスト参照
     yen = ""
     c=country.get()
     try:
          flt = float(box1.get()) #ユーザーが入れた値（box.get()）を数値に変換
     except ValueError:
          error ["text"] = "無効な値が入力されました" #エラーがあった場合は値が返される
          yen = "-----"
     else:
          yen = rate_dic[c] * flt
     finally:
          box2.delete(0,tk.END)
          box2.insert(tk.END,yen)

#------見えてないエラー対応用テキスト-----------
error = tk.Label (fg="#FF0000",
                  font=("メイリオ",15,"bold"),
                  bg="#e5ffcc")     #foreground 文字色
error.place(relx=0.5,rely=0.7,anchor=tk.CENTER)

# ---------------GUI-----------------------
text1 = tk.Label(text="為替レート計算",
                 font = ("メイリオ",20,""),
                 pady = 10,bg = "#e5ffcc")  #パディングy
text1.pack()


#-------日付をスクレイピング------------------
date_s = kekka.find_all("p", class_="tRight")
print(date_s)
#日付の取得
date_text = date_s[0].text if date_s else "NO Date" #エラーチェック
print(date_text)
#date_strにスクレイピング日付を設定
date_str = date_text
date = tk.Label(text=date_str,
              font = ("メイリオ",10,""),
              pady = 5,bg="#e5ffcc")
date.place(relx=0.5,rely=0.15,anchor=tk.CENTER)
#-----------------------------------------------

#テキストbox1
box1=tk.Entry(width=10,font=("",20,""),justify=tk.RIGHT) # 右側に配置
box1.place(relx=0.1,rely=0.25) #配置比率0は左上1.0はx一番右y一番下
#セレクトbox：国
country=ttk.Combobox(width=25,font=("",20,""))
# country["values"]=("米国ドル","ユーロ","英ポンド,スイスフラン,オーストラリアドル,ニュージーランドドル)
country["values"]=list(rate_dic.keys())    #リストっぽいもの→ちゃんとしたリスト化
country.current(0)  #コンボボックスの選択肢の中で、0番目（最初）の項目を初期値とする
country.place(relx=0.4,rely=0.25)

#ボタン
btn=tk.Button(text="計算する",
              font=("メイリオ",22,"bold"),
              background="#9effce",
              width=10,
              command=late_ex)        #関数が実行
btn.place(relx=0.5,rely=0.5,anchor=tk.CENTER) 

#出力box
box2=tk.Entry(width=15,
              font=("",25,""),
              justify=tk.RIGHT)
box2.place(relx=0.5,rely=0.8,anchor=tk.CENTER)

yen= tk.Label(text="円",
              font=("",15,""),
              bg="#e5ffcc")
yen.place(relx=0.72,rely=0.79)


#---------画像指定 #写真型---------------------------
icon=tk.PhotoImage(file="image/yen.png") #画像はpngのみOK
#画面型tkの上にレイアウトのキャンバス型を載せる
layout=tk.Canvas(width=140,height=170,bg="#e5ffcc")
layout.place(relx=0.03,rely=0.5)
#写真を表示
layout.create_image(8,10,image=icon,anchor=tk.NW)
#------------------------------------------------

#画面を閉じないように
root.mainloop()
