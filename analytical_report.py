import csv
from lib2to3.pytree import convert
import sys


def get_failure_count(path='reports/_stats.csv'):
    with open(path, 'r') as file:
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

if __name__ == '__main__':
    path = sys.argv[1]
    warning_threshold = sys.argv[2] #20
    failure_threshold = sys.argv[3] #30
    requests = get_request_count()
    failure = get_failure_count(path)

    failed_percent = float(failure) / float(requests) * float(100)

    if failed_percent >= float(warning_threshold):
        status = "fail"
    elif failed_percent >= float(failure_threshold):
        status = "warning"
    else:
        status = "pass"

    print(status)

