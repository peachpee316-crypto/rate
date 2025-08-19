"""為替計算アプリ"""

import tkinter as tk,tkinter.ttk as ttk
import datetime as dt

root=tk.Tk()
root.title("為替計算アプリ")
root.minsize(600,400)
root["bg"]="#d6eaff"

# -----------関数------------
# rate_dic={"米国ドル":148.47,
#           "英国ポンド":198.74,
#           "人民元":20.6829,
#           "韓国ウオン":0.1067}


#csvファイルから読み込む #読み込めない！
def load_rates():
     rate_dic={} 
     print("csv読み込み開始")    #辞書     
     with open("file/rate.csv","r", encoding="utf-8") as fp:
          for val in fp:
               temp=val.strip().split(",")
               if len(temp)>=2:
                    key=temp[0]  #通貨名「米ドル」を取り出す
                    val=float(temp[1])
                    rate_dic[key]=val
     #return は関数が外部に値を渡すための仕組、関数の中だけで作った変数（rate_dicなど）は、その関数の外では使えません          
     return rate_dic
rate_dic=load_rates()  #load_rates()は辞書を返す関数で呼び出さないと実行されない。初めて辞書が作られた。

#レート計算
def late_ex():
     error["text"]= "" #初めにtextのエラーメッセージを空に設定。※見えてないエラー対応テキスト参照
     yen=""
     c=country.get()
     try:
          flt=float(box1.get()) #その後、ユーザーが入れた値（box.get()）を数値に変換
     except ValueError:
          error["text"]="無効な値が入力されました" #エラーがあった場合は値が返される
          yen="-----"
     else:
          yen=rate_dic[c]*flt
     finally:
          box2.delete(0,tk.END)
          box2.insert(tk.END,yen)
#--------------------------------------------
#見えてないエラー対応用テキスト
error =tk.Label(fg="#FF0000",
                font=("メイリオ",15,"bold"),
                bg="#d6eaff")     #foreground 文字色
error.place(relx=0.5,rely=0.7,anchor=tk.CENTER)

# ------------------------------------------

text1=tk.Label(text="為替計算",
              font=("メイリオ",20,""),
              pady=10,bg="#d6eaff")  #パディングy
text1.pack()

date_str=dt.date.today()
date=tk.Label(text=date_str,
              font=("メイリオ",10,""),
              pady=5,bg="#d6eaff")
date.place(relx=0.5,rely=0.2,anchor=tk.CENTER)


#テキストbox1
box1=tk.Entry(width=10,font=("",20,""),justify=tk.RIGHT) # 右側に配置
box1.place(relx=0.1,rely=0.25) #配置比率0は左上1.0はx一番右y一番下
#セレクトbox：国
country=ttk.Combobox(width=20,font=("",20,""))
# country["values"]=("米国ドル","英国ポンド","人民元","韓国ウオン")
country["values"]=list(rate_dic.keys())    #リストっぽいもの→ちゃんとした下リスト化
country.current(0)  #コンボボックスの選択肢の中で、0番目（最初）の項目を初期値として選ぶ
country.place(relx=0.4,rely=0.25)

#ボタン
btn=tk.Button(text="計算する",
              font=("メイリオ",22,"bold"),
              background="#9999ff",
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
              bg="#d6eaff")
yen.place(relx=0.75,rely=0.79)

#画像指定 #写真型
icon=tk.PhotoImage(file="image/yen.png") #画像はpngのみOK
#画面型tkの上にレイアウトのキャンバス型を載せる
layout=tk.Canvas(width=140,height=170,bg="#c1e0ff")
layout.place(relx=0.03,rely=0.5)
#写真を表示
layout.create_image(8,10,image=icon,anchor=tk.NW)


#画面を閉じないように
root.mainloop()