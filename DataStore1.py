#random data generator
import random
import csv
import time 
import select 
import sys

def randomdata():
    return random.randint(0, 100), random.randint(100, 200), random.randint(200, 300), random.randint(300, 400)

def append_to_csv(data, filename='datastore.csv'):
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)

def sum_rows(filename='datastore.csv'):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            print(sum(map(int, row)))

while True:
    data = randomdata()
    #wait 2 sec
    time.sleep(2)
    
    append_to_csv(data)
    
    ready, _, _ = select.select([sys.stdin], [], [], 0)
    if ready:
        user_input = input()
        # Check if the user wants to stop
        if user_input.strip().lower() == 'stop':
            break

#when you write down 'stop' in the terminal you will see all sums of the rows
def main ():
    sum_rows()
main()