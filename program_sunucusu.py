
import socket
import threading
import json

YARISMACI_HOST = '127.0.0.1'
YARISMACI_PORT = 4337

JOKER_HOST = '127.0.0.1'
JOKER_PORT = 4338

sorular = [
    {
        "soru": "Python hangi yıl geliştirilmiştir?",
        "secenekler": {"A": "1991", "B": "2000", "C": "1989", "D": "2010"},
        "dogru": "A"
    },
    {
        "soru": "Türkiye'nin başkenti neresidir?",
        "secenekler": {"A": "İstanbul", "B": "Ankara", "C": "İzmir", "D": "Bursa"},
        "dogru": "B"
    },
    {
        "soru": "Hangisi bir programlama dilidir?",
        "secenekler": {"A": "HTML", "B": "Python", "C": "CSS", "D": "Photoshop"},
        "dogru": "B"
    },
    {
        "soru": "En büyük gezegen hangisidir?",
        "secenekler": {"A": "Mars", "B": "Venüs", "C": "Jüpiter", "D": "Dünya"},
        "dogru": "C"
    },
    {
        "soru": "Elektronun yükü nedir?",
        "secenekler": {"A": "Pozitif", "B": "Negatif", "C": "Yüksüz", "D": "Çift Yüklü"},
        "dogru": "B"
    }
]

oduller = [
    "Linç Yükleniyor",
    "Önemli olan katılmaktı",
    "İki birden büyüktür",
    "Buralara kolay gelmedik",
    "Sen bu işi biliyorsun",
    "Harikasın"
]

def joker_iste(joker_turu, soru_dict):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as joker:
            joker.connect((JOKER_HOST, JOKER_PORT))
            mesaj = {
                'type': joker_turu,
                'question': soru_dict['soru'],
                'choices': list(soru_dict['secenekler'].keys()),
                'correct': soru_dict['dogru']
            }
            joker.sendall(json.dumps(mesaj).encode())
            cevap = joker.recv(4096).decode()
            return json.loads(cevap)
    except Exception as e:
        print("Joker sunucusuna bağlanırken hata:", e)
        return None

def handle_client(conn, addr):
    print(f"[+] Yarışmacı bağlandı: {addr}")
    joker_haklari = {"S": True, "Y": True}

    for i, soru in enumerate(sorular):
        soru_mesaji = {
            "index": i + 1,
            "soru": soru["soru"],
            "secenekler": soru["secenekler"],
            "jokerler": {k: v for k, v in joker_haklari.items() if v}
        }
        conn.sendall(json.dumps(soru_mesaji).encode())
        cevap = conn.recv(1024).decode().strip().upper()

        if cevap in ["S", "Y"] and joker_haklari.get(cevap):
            joker_sonucu = joker_iste(cevap, soru)
            if joker_sonucu:
                conn.sendall(json.dumps(joker_sonucu).encode())
                cevap = conn.recv(1024).decode().strip().upper()
            joker_haklari[cevap] = False

        if cevap == soru["dogru"]:
            continue  # doğruysa bir sonraki soruya geç
        else:
            mesaj = {"mesaj": f"Yarışma sona erdi.  {oduller[i]}"}
            conn.sendall(json.dumps(mesaj).encode())
            print("[-] Yanlış cevap. Oyun bitti.")
            return

    mesaj = {"mesaj": f" Tüm soruları doğru bildiniz. {oduller[5]}"}
    conn.sendall(json.dumps(mesaj).encode())
    print("[+] Tüm sorular başarıyla tamamlandı!")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((YARISMACI_HOST, YARISMACI_PORT))
        server.listen()
        print(f"Program Sunucusu {YARISMACI_HOST}:{YARISMACI_PORT} dinleniyor...")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
