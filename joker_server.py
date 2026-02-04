import socket
import json
import random

HOST = '127.0.0.1'
PORT = 4338

def handle_request(request):
    data = json.loads(request)
    question = data['question']
    choices = data['choices']
    correct = data['correct']
    joker_type = data['type']

    if joker_type == 'S':  # Seyirciye Sorma
        percentages = {}
        correct_percentage = random.randint(40, 70)
        remaining = 100 - correct_percentage
        other_choices = [c for c in choices if c != correct]
        random.shuffle(other_choices)
        split = [random.randint(0, remaining) for _ in range(2)]
        split.append(remaining - sum(split))
        for i, c in enumerate(other_choices):
            percentages[c] = split[i]
        percentages[correct] = correct_percentage
        response = {'type': 'S', 'percentages': percentages}

    elif joker_type == 'Y':  # Yarı Yarıya
        incorrects = [c for c in choices if c != correct]
        eliminated = random.sample(incorrects, 2)
        remaining = [c for c in choices if c not in eliminated]
        response = {'type': 'Y', 'remaining': remaining}

    return json.dumps(response)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Joker sunucusu {HOST}:{PORT} dinleniyor...")

    while True:
        conn, addr = server.accept()
        with conn:
            data = conn.recv(4096).decode()
            if not data:
                continue
            response = handle_request(data)
            conn.sendall(response.encode())

