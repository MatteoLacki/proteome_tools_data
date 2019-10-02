from pathlib import Path
import pandas as pd
from pprint import pprint


res_path = Path(r"D:/projects/proteome_tools/RES/pool2")

def iter_res_folders(res_path):
    for p in res_path.glob('*/*'):
        date, sample_no = p.name[1:].split('_')
        yield p, date


reports = []
missing = []

for p, date in iter_res_folders(res_path):
    try:
        date = pd.to_datetime("20{}/{}/{}".format(date[0:2], date[2:4], date[4:6]))
        report = pd.read_csv(p/'report.csv')
        report['date'] = date
        reports.append(report)
    except FileNotFoundError:
        missing.append((p, date))

RES = pd.concat(reports)
RES.to_csv("D:/projects/proteome_tools/report.csv")

len(reports)
pprint(missing)
len(missing)

RES.columns
RES_an = RES.groupby('acquired_name')

RES_an.size()
