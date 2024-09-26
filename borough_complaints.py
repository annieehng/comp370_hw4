"""
Build a python-based command line tool borough_complaints.py that uses argparse 
to provide a UNIX-style command which outputs the number of each complaint type per 
borough for a given (creation) date range.

The command should take arguments in this way:
    borough_complaints.py -i <the input csv file> -s <start date> -e <end date> [-o <output file>]

If the output argument isn’t specified, then just print the results (to stdout)

Results should be printed in a csv format like:
	complaint type, borough, count
	derelict vehicles, Queens, 236
	derelict vehicles, Bronx, 421
	…

Note that borough_complaints.py -h should print a relatively nice help message thanks to argparse.
Commit your script, but not the data to your git repo.

"""

# output the number of each complaint type per borough for a given (creation) data range 

import argparse
import csv
from collections import Counter
from datetime import datetime

def parse_arguments(): # parse the arguments from the command

    parser = argparse.ArgumentParser( # helpful message for the user 
        description="CLI tool to track the complaint types and count the complaint types by borough within a date range."
    )

    parser.add_argument("-i", "--input", required=True, help="Input CSV file")
    parser.add_argument("-s", "--start", required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("-e", "--end", required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("-o", "--output", help="Optional output file for results (CSV format)")
    
    return parser.parse_args() # args


def is_within_date_range(complaint_date, start_date, end_date): # checking for valid date 

    complaint_dt = datetime.strptime(complaint_date, '%Y-%m-%d')
    return start_date <= complaint_dt <= end_date

def process_complaints(input_file, start_date, end_date): # process the complaints and create our features on our data

    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        complaints_counter = Counter()
        for row in reader:
            complaint_date = row['creation_date'] # select date column
            borough = row['borough'] # select borough column
            complaint_type = row['complaint_type'] # select the complaint type column
            if is_within_date_range(complaint_date, start_date, end_date): # check if date is within the range given 
                complaints_counter[(complaint_type, borough)] += 1

    return complaints_counter

def output_results(complaints_counter, output_file=None): # output the results 

    if output_file:
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['complaint type', 'borough', 'count']) # our fields of the csv file we making 
            for (complaint_type, borough), count in complaints_counter.items():
                writer.writerow([complaint_type, borough, count])
    else:
        print("complaint type, borough, count")
        for (complaint_type, borough), count in complaints_counter.items():
            print(f"{complaint_type}, {borough}, {count}")

# main function
def main():
   
    args = parse_arguments()
    start_date = datetime.strptime(args.start, '%Y-%m-%d')
    end_date = datetime.strptime(args.end, '%Y-%m-%d')
    complaints_counter = process_complaints(args.input, start_date, end_date)
    output_results(complaints_counter, args.output) 

if __name__ == "__main__":
    main()