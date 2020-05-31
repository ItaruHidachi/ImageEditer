import cv2
import glob
import os
import numpy as np
import tkinter
from tkinter import messagebox
from tkinter import filedialog

#ボタンがクリックされたら実行
def reference_button_click1():
    file_path1 = tkinter.filedialog.askdirectory()
    input_box1.insert(tkinter.END, file_path1)

def reference_button_click2():
    file_path2 = tkinter.filedialog.askdirectory()
    input_box2.insert(tkinter.END, file_path2)

def imageEdit():
    file_path1 = input_box1.get()
    file_path2 = input_box2.get()
    #ファイルパス
    file_su = os.listdir(file_path1)
    files_dir = [f for f in file_su if os.path.isdir(os.path.join(file_path1, f))]
    print("＝＝＝下記のフォルダが検出されました＝＝＝")
    print(files_dir)
    print("＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝")
    #検出したフォルダの数分繰り返し
    for f in range(len(files_dir)):
        strnames = str(files_dir[f])
        #rusultにフォルダが存在しない場合フォルダを作成
        if os.path.isdir(file_path2+"/"+strnames)==False:
            print(file_path2+"フォルダに"+strnames+"フォルダが存在しないため作成します")
            os.mkdir(file_path2+"/"+strnames)
        #jpg画像が何枚あるか検知
        jpg_hai = glob.glob(file_path1+"/"+strnames+"/*.JPG")
        print(strnames+"フォルダに"+str(len(jpg_hai))+"枚のjpgファイルを検出")
        print("～"+strnames+"フォルダ画像処理開始～")
        #フォルダ内の画像の枚数分繰り返し
        for i in range(len(jpg_hai)):
            num = i + 1
            #傾け角度
            angle = 15
            print("　{}枚目処理中".format(num))
            filename = jpg_hai[i]
            # オリジナルデータ読み取り
            img_origin = cv2.imread(filename, -1)
            # 角度数値読み取り
            if cb1n1.get():
                angles = EditBox1.get()
                angles_list = str(angles).split(",")
            else:
                angles_list = ["0"]
            # 角度の値だけ繰り返す
            for ang_i in range(len(angles_list)):
                # 角度
                rows,cols,c = img_origin.shape
                origin_rotate = cv2.getRotationMatrix2D((cols/2,rows/2),int(angles_list[ang_i]),1)
                img_Rotate = cv2.warpAffine(img_origin,origin_rotate,(cols,rows))
                cv2.imwrite(file_path2+"/"+strnames+"/"+strnames+"_normal_"+str(angles_list[ang_i])+" ("+str(num)+").jpg", img_Rotate)
                #ぼかし
                filt = EditBox2.get()
                filt_list = str(filt).split(",")
                # ぼかしの数だけ繰り返す
                if cb1n2.get():
                    for filt_i in range(len(filt_list)):
                        img_filter = cv2.blur(img_Rotate,(int(filt_list[filt_i]),int(filt_list[filt_i])))
                        cv2.imwrite(file_path2+"/"+strnames+"/"+strnames+"_filter_"+str(angles_list[ang_i])+"["+filt_list[filt_i]+"_"+filt_list[filt_i]+"]_("+str(num)+").jpg", img_filter)
                else:
                    pass
                #閾値処理
                if cb1n3.get():
                    img_gray = cv2.cvtColor(img_Rotate, cv2.COLOR_BGR2GRAY)
                    th,img_th = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
                    cv2.imwrite(file_path2+"/"+strnames+"/"+strnames+"_th_"+str(angles_list[ang_i])+" ("+str(num)+").jpg", img_th)
                else:
                    pass
        print("～"+strnames+"フォルダ画像処理完了～")
    print("＝＝＝＝＝＝＝全画像処理完了＝＝＝＝＝＝＝")
    print("")


def sngle_onoff():
    if cb1n1.get():
        EditBox1.config(state="normal")
    else:
        EditBox1.config(state="disable")

def filt_onoff():
    if cb1n2.get():
        EditBox2.config(state="normal")
    else:
        EditBox2.config(state="disable")

#ウインドウの作成
root = tkinter.Tk()
root.title("画像加工ソフト")
root.geometry("720x480")

#画像編集元データパス
input_label1 = tkinter.Label(text="●画像編集元データパス")
input_label1.place(x=10, y=20)
input_box1 = tkinter.Entry(width=100)
input_box1.place(x=10, y=50)
button1 = tkinter.Button(text="参照する",command=reference_button_click1)
button1.place(x=620, y=45)

#編集先設置パス
input_label2 = tkinter.Label(text="●編集先設置パス")
input_label2.place(x=10, y=90)
input_box2 = tkinter.Entry(width=100)
input_box2.place(x=10, y=120)
button2 = tkinter.Button(text="参照する",command=reference_button_click2)
button2.place(x=620, y=115)

#使用オプション
input_label5 = tkinter.Label(text="●オプション")
input_label5.place(x=10, y=160)
cb1n1 = tkinter.BooleanVar()
cb1 = tkinter.Checkbutton(
    variable=cb1n1,
    text='傾き',
    onvalue='ON',
    offvalue='OFF',
    command=sngle_onoff)
cb1.place(x=10, y=180)
cb1n2 = tkinter.BooleanVar()
cb2 = tkinter.Checkbutton(
    variable=cb1n2,
    text='ぼかし',
    onvalue='ON',
    offvalue='OFF',
    command=filt_onoff)
cb2.place(x=110, y=180)
cb1n3 = tkinter.BooleanVar()
cb3 = tkinter.Checkbutton(
    variable=cb1n3,
    text='閾値処理',
    onvalue='ON',
    offvalue='OFF')
cb3.place(x=210, y=180)

#傾き度数記入
input_label3 = tkinter.Label(text="●傾き度数調整(『,』区切り記入)")
input_label3.place(x=10, y=230)
EditBox1 = tkinter.Entry()
EditBox1.insert(tkinter.END,"0,10,-10")
EditBox1.place(x=10, y=260)
EditBox1.config(state="disable")

#ぼかし記入
input_label4 = tkinter.Label(text="●ぼかし調整(『,』区切り記入)")
input_label4.place(x=10, y=300)
EditBox2 = tkinter.Entry()
EditBox2.insert(tkinter.END,"100")
EditBox2.place(x=10, y=330)
EditBox2.config(state="disable")

#実行ボタン
button3 = tkinter.Button(text="実行",command=imageEdit)
button3.place(x=640, y=400)

#ウインドウの描画
root.mainloop()