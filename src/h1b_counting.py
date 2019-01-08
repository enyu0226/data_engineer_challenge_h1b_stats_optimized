import csv
import re
import sys
from collections import Counter
from itertools import groupby
import heapq

# accept arguments
args = sys.argv

# read csv file to list-of-lists
with open(args[1], 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    my_list = list(reader)


# find column indices
STATUS = [i for i, s in enumerate(my_list[0]) if bool(re.search('STATUS', s.upper()))][0]
SOC_NAME = [i for i, s in enumerate(my_list[0]) if bool(re.search('SOC_NAME', s.upper()))][0]
WORKSITE_STATE = [i for i, s in enumerate(my_list[0]) if bool(re.search('WORK.*_STATE', s.upper()))][0]


# get SOCs and worksites for certified observations
SOC_NAME_list = [row[SOC_NAME] for row in my_list if ('CERTIFIED' == row[STATUS].upper())]
WORKSITE_STATE_list = [row[WORKSITE_STATE] for row in my_list if ('CERTIFIED' == row[STATUS].upper())]


# use collections.Counter() to count SOCs, then sort on count (high to low) followed by alphabetical order
SOC_NAME_dict = Counter(SOC_NAME_list)
SOC_NAME_total = sum(SOC_NAME_dict.values())
# uses min-heap to store only top k element to reduce locating the top k element to O(nlogk) runtime as opposed to O(nlogn) using sorting.
SOC_NAME_Top_10=heapq.nlargest(10, SOC_NAME_dict.items(), key=lambda x: (x[1], x[0]))

# use collections.Counter() to count states, then sort on count (high to low) followed by alphabetical order
WORKSITE_STATE_dict = Counter(WORKSITE_STATE_list)
WORKSITE_STATE_total = sum(WORKSITE_STATE_dict.values())
WORKSITE_STATE_Top_10=heapq.nlargest(10, WORKSITE_STATE_dict.items(), key=lambda x: (x[1], x[0]))

# helper function to pretty print percents
def percent(num1, num2):
    return '{0:.1f}%'.format(100 * num1 / num2)


# write sorted SOCs to csv file
with open(args[2], 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
    for soc, count in SOC_NAME_Top_10:
       writer.writerow([soc, count, percent(count, SOC_NAME_total)])

# write sorted states to csv file
with open(args[3], 'w', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
    for state, count in WORKSITE_STATE_Top_10:
       writer.writerow([state, count, percent(count, WORKSITE_STATE_total)])

