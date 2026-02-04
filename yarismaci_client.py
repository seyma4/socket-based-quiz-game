import tkinter as tk
from tkinter import ttk
import socket
import json
from tkinter import messagebox

class YarismaciGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Kim Milyoner Olmak İster? - Yarışmacı")
        self.master.geometry("600x450")
        self.master.configure(bg="#1E1E2F")

        style = ttk.Style()
        style.theme_use('clam')

        # Oval stil (cevap butonları)
        style.configure("Rounded.TButton",
                        foreground="white",
                        background="#3A3A5C",
                        font=("Poppins", 12, "bold"),
                        padding=10,
                        borderwidth=0,
                        relief="flat")
        style.map("Rounded.TButton",
                  background=[("active", "#2F2F4D")])  # Hover: biraz daha koyu

        # Joker buton stili
        style.configure("Joker.TButton",
                        foreground="black",
                        background="#FFC107",
                        font=("Poppins", 11, "bold"),
                        padding=10,
                        borderwidth=0,
                        relief="flat")
        style.map("Joker.TButton",
                  background=[("active", "#E0A800")])  # Hover: koyulaşma

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(("127.0.0.1", 4337))

        self.kullanilan_jokerler = {"S": False, "Y": False}

        self.soru_label = tk.Label(master, text="", wraplength=500,
                                   font=("Poppins", 14, "bold"), bg="#1E1E2F", fg="white")
        self.soru_label.pack(pady=20)

        self.secenek_butonlari = {}
        for secenek in ["A", "B", "C", "D"]:
            btn = ttk.Button(master, text="", style="Rounded.TButton",
                             command=lambda s=secenek: self.cevap_gonder(s))
            btn.pack(pady=4)
            self.secenek_butonlari[secenek] = btn

        joker_frame = tk.Frame(master, bg="#1E1E2F")
        joker_frame.pack(pady=15)

        self.joker_butonlari = {}
        self.joker_butonlari["S"] = ttk.Button(joker_frame, text="Seyirciye Sorma",
                                               style="Joker.TButton",
                                               command=lambda: self.joker_kullan("S"))
        self.joker_butonlari["S"].grid(row=0, column=0, padx=10)

        self.joker_butonlari["Y"] = ttk.Button(joker_frame, text="Yarı Yarıya",
                                               style="Joker.TButton",
                                               command=lambda: self.joker_kullan("Y"))
        self.joker_butonlari["Y"].grid(row=0, column=1, padx=10)

        self.sonraki_soru()

    def sonraki_soru(self):
        self.temizle()
        mesaj = self.conn.recv(4096).decode()
        mesaj = json.loads(mesaj)

        if "soru" in mesaj:
            self.soru_label.config(text=mesaj["soru"])

            for secenek, yazi in mesaj["secenekler"].items():
                self.secenek_butonlari[secenek]["text"] = f"{secenek}) {yazi}"
                self.secenek_butonlari[secenek]["state"] = "normal"

            for joker in ["S", "Y"]:
                if not self.kullanilan_jokerler[joker] and joker in mesaj["jokerler"]:
                    self.joker_butonlari[joker]["state"] = "normal"
                else:
                    self.joker_butonlari[joker]["state"] = "disabled"

        elif "mesaj" in mesaj or "odul" in mesaj:
            # Yarışma bitti
            icerik = mesaj.get("mesaj", mesaj.get("odul", "Oyun sona erdi."))
            messagebox.showinfo("Oyun Bitti", icerik)
            self.master.quit()

    def cevap_gonder(self, secenek):
        self.conn.sendall(secenek.encode())
        self.sonraki_soru()

    def joker_kullan(self, joker_turu):
        self.conn.sendall(joker_turu.encode())
        sonuc = self.conn.recv(4096).decode()
        joker_verisi = json.loads(sonuc)

        if joker_verisi["type"] == "S":
            yuzdeler = joker_verisi["percentages"]
            for secenek in self.secenek_butonlari:
                metin = self.secenek_butonlari[secenek]["text"]
                if secenek in yuzdeler:
                    self.secenek_butonlari[secenek]["text"] = f"{metin} (%{yuzdeler[secenek]})"
                else:
                    self.secenek_butonlari[secenek]["state"] = "disabled"

        elif joker_verisi["type"] == "Y":
            kalanlar = joker_verisi["remaining"]
            for secenek in self.secenek_butonlari:
                if secenek not in kalanlar:
                    self.secenek_butonlari[secenek]["state"] = "disabled"

        self.joker_butonlari[joker_turu]["state"] = "disabled"
        self.kullanilan_jokerler[joker_turu] = True

    def temizle(self):
        for secenek in self.secenek_butonlari:
            self.secenek_butonlari[secenek].config(text="", state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = YarismaciGUI(root)
    root.mainloop()
