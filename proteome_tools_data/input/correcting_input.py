from pathlib import Path
import pandas as pd
import json
import re
from collections import Counter
import numpy as np

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', -1)#display whole column without truncation

pt = Path("/mnt/ms/restoredData/proteome_tools")

with open(pt/'pool1.json','r', encoding ="utf-8") as f:
    pool1 = json.load(f)

P1 = {p:f for p,f in pool1}

with open(pt/'pool1_wrong.json','r', encoding ="utf-8") as f:
    pool1_wrong = json.load(f)

W1 = {p:f for p,f in pool1_wrong}
C = {p: P1[p] for p in P1 if P1[p] != W1[p]}
proj2fix = {Path(p).stem for p in C}

DIA = pd.read_csv(pt/'DIA.csv').set_index('Raw_File')
DIA2FIX  = DIA.loc[proj2fix]

DIA2FIX.to_csv(pt/'dia2fix.csv')

pool1fix = list(C.items())

with open(pt/'pool1fix.json', 'w', encoding ="utf-8") as f:
    json.dump(pool1fix, f, indent=4)