import socket
import random
from stats_manager.manager import StatManager
import time

HOST = "localhost"
PORT = 65432

msg = ""
n_states = 10

ACTIONS = [
    "BuildHospital",
    "BuildPark",
    "BuildFactory",
    "BuildTransport",
    "BuildEducationInstitutes",
    "BuildResidentialBuilding",
    "BuildOffices",
    "DevelopScienceCenter",
    "BuildFarm",
    "DevelopRenewableEnergy",
]

population = []
pop_size = 16


def init_population():
    # initialize population with brains
    # each will be an object containing a genome and statmanager
    for _ in range(pop_size):
        obj = StatManager()
        population.append(obj)
    pass


def create_message():
    full_message = ""
    for p in population:
        (action, action_number) = p.sample()
        p.take_action(action)
        full_message += combine_message(p.all_stats.values(), action_number) + ":"
    return full_message[:-1]


def combine_message(stats, action_number):
    msg = ",".join(str(round(v, 4)) for v in stats)
    msg += "," + str(action_number)
    return msg


def main():
    init_population()

    # start server (socket)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set socket options
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print(f"{PORT} listening...")

    s.listen()
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    while True:
        msg = create_message()
        conn.sendall(str(msg).encode())

        cmd = conn.recv(1024).decode()

        if "next" in cmd:
            continue

        if "exit" in cmd:
            break


main()
