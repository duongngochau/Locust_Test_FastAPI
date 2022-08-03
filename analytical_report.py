import csv
from lib2to3.pytree import convert
import re


def get_failure_count():
    with open('reports/_stats.csv', 'r') as file:
        reader = csv.DictReader(file)
        for each_row in reader:
            if each_row["Name"] == "Aggregated":
                return each_row["Failure Count"]

def get_request_count():
    with open('reports/_stats.csv', 'r') as file:
        reader = csv.DictReader(file)
        for each_row in reader:
            if each_row["Name"] == "Aggregated":
                return each_row["Request Count"]


requests = get_request_count()
failure = get_failure_count()

per_fail = float(failure) / float(requests) * float(100)

if per_fail >= 60:
    status = "fail"
elif per_fail <= 20:
    status = "pass"
else:
    status = "warning"

print(status)

