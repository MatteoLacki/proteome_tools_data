from pathlib import Path
import pandas as pd
from pprint import pprint
import json
import logging

from vodkas import plgs, wx2csv
from proteome_tools_data.file_iteration import all_res

existing = {f.stem for f in all_res}
proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
pool2_path = proj_folder/'RES'/'pool2'
res_folder = Path(r"D:/projects/proteome_tools/RES")
out_folder = res_folder/"pool2"

with open(proj_folder/"pool2.json", 'r') as f:
    settings = json.load(f)

pool2 = {Path(raw).stem for raw, fasta in settings}
missing = pool2 - existing
missing_files = [(f,fas) for f,fas in settings if Path(f).stem in missing]



logging.basicConfig(filename=out_folder/"pool2.log",
                    format='PLGS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = logging.getLogger('PLGS')
timeout = 8 * 60 # 8 hours timeout [in minutes]
    
for rawdatapath, fastapath in missing_files:
    rawdatapath = Path(rawdatapath)
    fastapath = Path(fastapath)
    raw_folder = rawdatapath.stem
    final_out_folder = out_folder/raw_folder[0:5]/raw_folder
    for low_energy_thr in [300, 400, 500]:
        try:
            ok = plgs(rawdatapath,
                      final_out_folder,
                      low_energy_thr=low_energy_thr,
                      fastas=fastapath,
                      timeout_apex3d=timeout,
                      timeout_peptide3d=timeout,
                      timeout_iadbs=timeout)

            workflow_xml = next(final_out_folder.glob('*_IA_workflow.xml'))
            df, _ = wx2csv(workflow_xml, final_out_folder/'report.csv')
            break
        except Exception as e:
            logger.warning(repr(e))
