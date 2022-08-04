import csv
from lib2to3.pytree import convert
import sys
import logging


logger = logging.getLogger()
logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s   %(name)-8s %(levelname)-10s %(message)s')



def get_failure_count(path='reports/_stats.csv'):
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for each_row in reader:
            if each_row["Name"] == "Aggregated":
                return each_row["Failure Count"]

def get_request_count(path='reports/_stats.csv'):
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for each_row in reader:
            if each_row["Name"] == "Aggregated":
                return each_row["Request Count"]

def get_failed_percent(path, warning_threshold, failure_threshold):
    requests = get_request_count(path)
    failure = get_failure_count(path)

    failed_percent = round(float(failure) / float(requests) * float(100), 2)

    logger.info(f"Current failed: {failed_percent}%")
    logger.info(f"Unstable threshold: {warning_threshold}%")
    logger.info(f"Failure threshold: {failure_threshold}%")

    if failed_percent >= float(failure_threshold):
        logger.error(
            f"Current failed ({failed_percent}%) "
            + ">= " 
            + f"Failure Threshold ({failure_threshold}%)")
        logger.error("Failure")
        status = "fail"
    elif failed_percent >= float(warning_threshold):  
        logger.warning(
            f"Current failed ({failed_percent}%) "
            + ">= " 
            + f"Warnings Threshold ({warning_threshold}%)")
        logger.warning("Unstable")
        status = "warnings"
    else:
        status = "pass"
    return status

if __name__ == '__main__':
    path = sys.argv[1]
    warning_threshold = sys.argv[2] #20
    failure_threshold = sys.argv[3] #30
    print(get_failed_percent(path, warning_threshold, failure_threshold))
