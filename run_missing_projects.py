from pathlib import Path
import pandas as pd
from pprint import pprint
import json
import logging

from vodkas import plgs, wx2csv

res_path = pool2 = Path("D:/projects/proteome_tools/RES/pool2")
present = {f.stem for f in res_path.glob('*/*')}

with_reports = {p.parent.stem for p in res_path.glob('*/*/report.csv')}
missing_reports = present - with_reports
present -= missing_reports

# reports = []
# for mr in missing_reports:
#     df = wx2csv(res_path/mr[0:5]/mr/f"{mr}_IA_workflow.xml", res_path/mr[0:5]/mr/'report.csv')
#     reports.append(df)


proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
with open(proj_folder/"pool2.json", 'r') as f:
    settings = json.load(f)

missing_files = [(f,fas) for f,fas in settings if Path(f).stem not in present]

with open(pool2/"missing.json", 'w') as f:
    json.dump([a for a,b in missing_files], f, indent=4)

logging.basicConfig(filename=pool2/"pool2.log",
                    format='PLGS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = logging.getLogger('PLGS')
timeout = 8 * 60 # 8 hours timeout [in minutes]

    
for rawdatapath, fastapath in missing_files:
    rawdatapath = Path(rawdatapath)
    fastapath = Path(fastapath)
    raw_folder = rawdatapath.stem
    out_folder = pool2/raw_folder[0:5]/raw_folder
    for low_energy_thr in [300, 400, 500]:
        try:
            ok = plgs(rawdatapath,
                      out_folder,
                      low_energy_thr=low_energy_thr,
                      fastas=fastapath,
                      timeout_apex3d=timeout,
                      timeout_peptide3d=timeout,
                      timeout_iadbs=timeout)

            workflow_xml = next(out_folder.glob('*_IA_workflow.xml'))
            df, _ = wx2csv(workflow_xml, out_folder/'report.csv')
            break
        except Exception as e:
            logger.warning(repr(e))
