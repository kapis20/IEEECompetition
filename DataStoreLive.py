import threading
import tkinter as tk
from tkinter import messagebox
import random
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

def randomdata():
    return random.randint(0, 100), random.randint(100, 200), random.randint(200, 300), random.randint(300, 400)

def append_to_csv(data, filename='datastore.csv'):
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)

def sum_rows(filename='datastore.csv'):
    sums = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            sums.append(sum(map(int, row)))
    return sums

def generate_data():
    while not stop_event.is_set():
        data = randomdata()
        append_to_csv(data)
        sums = sum_rows()
        update_plot(sums)
        root.update()
        time.sleep(2)

def start_generating():
    global stop_event
    stop_event.clear()
    generate_data()

def stop_generating():
    global stop_event
    stop_event.set()

def update_plot(data):
    df = pd.DataFrame(data, columns=['Sum'])
    ax.clear()
    ax.plot(df)
    ax.set_title('Random Data Sums')
    ax.set_xlabel('Index')
    ax.set_ylabel('Sum')
    canvas.draw()

root = tk.Tk()
root.title("Random Data Generator")

start_button = tk.Button(root, text="Start Generating", command=start_generating)
start_button.pack()

stop_button = tk.Button(root, text="Stop Generating", command=stop_generating)
stop_button.pack()

# Create matplotlib figure and canvas
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Initial plot
update_plot([])

# Event to control the generation loop
stop_event = threading.Event()

root.mainloop()
