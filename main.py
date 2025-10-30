import tkinter
from tkinter import messagebox
from cryptography.fernet import Fernet

window=tkinter.Tk()
window.title("SECRET NOTES")
window.minsize(width=300,height=600)
window.config(padx=30, pady=60)


#IMAGE
image_path = r"C:\Users\5ir\Desktop\tkinter_Secret_notes\top_secrets_img.png"
gorsel = tkinter.PhotoImage(file=image_path)
etiket = tkinter.Label(image=gorsel)
etiket.pack()

#TITLE
title_label=tkinter.Label(text="Enter your Title")
title_label.pack()
title_entry=tkinter.Entry(width=40)
title_entry.pack()

#SECRET
secret_label=tkinter.Label(text="Enter your Secret")
secret_label.pack()
secret_entry=tkinter.Text( width=30,height=10)
secret_entry.pack()

#MASTER KEY
master_key_label=tkinter.Label(text="Enter your Master Key")
master_key_label.pack()
master_key_entry=tkinter.Entry(width=40)
master_key_entry.pack()

#dictionary
passwords_and_secrets = {}

#FUNCTIONS
def crypto_string(secret):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    enc_text = fernet.encrypt(secret.encode())
    return key, enc_text

def decrypt_string(key, enc_text):
    fernet = Fernet(key)
    dec_text = fernet.decrypt(enc_text).decode()
    return dec_text

def kaydet():
    veri_title = title_entry.get().strip()
    veri_secret = secret_entry.get("1.0", "end-1c").strip()
    master_key_val = master_key_entry.get().strip()
    
    if not veri_title:
        messagebox.showinfo("Uyarı", "Lütfen bir başlık giriniz!")
        return
        
    if not veri_secret:
        messagebox.showinfo("Uyarı", "Lütfen bir gizli not giriniz!")
        return
        
    if not master_key_val:
        messagebox.showinfo("Uyarı", "Lütfen bir master key giriniz!")
        return
    
    with open("veri.txt", "a", encoding="utf-8") as dosya:
        dosya.write(f"Title: {veri_title}\n")
    
    key, enc_text = crypto_string(veri_secret)
    passwords_and_secrets[master_key_val] = (key, enc_text)
    with open("veri.txt", "a", encoding="utf-8") as dosya:
        dosya.write(f"Encrypted Secret: {enc_text.decode()}\n")
    
    # Entry ve Text temizle
    title_entry.delete(0, tkinter.END)
    master_key_entry.delete(0, tkinter.END)
    secret_entry.delete("1.0", tkinter.END)

def decrypt_secret():
    master_key_val = master_key_entry.get().strip()
    
    if master_key_val in passwords_and_secrets:
        key, enc_text = passwords_and_secrets[master_key_val]
        dec_text = decrypt_string(key, enc_text)
        secret_entry.delete("1.0", tkinter.END)
        secret_entry.insert("1.0", dec_text)
    else:
        secret_entry.delete("1.0", tkinter.END)
        secret_entry.insert("1.0", "Bu Master Key için kayit bulunamadi!")

#button save
save_button=tkinter.Button(text="Save & Encrypt",command=kaydet)
save_button.pack()
#button decyrpt
decyrpt_button=tkinter.Button(text="Decyrpt",command=decrypt_secret)
decyrpt_button.pack()

window.mainloop()