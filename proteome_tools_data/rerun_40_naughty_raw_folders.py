"""Here we rerun the 40 naughty raw folders that resulted in nothing but pain."""

import logging
import numpy as np
import pandas as pd
from pathlib import Path
from pprint import pprint
from subprocess import TimeoutExpired
from vodkas.logging import get_logger
from vodkas import plgs, wx2csv

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)

outlook = pd.read_csv(Path("D:/projects/proteome_tools/RES/outlook.csv"))
coverages = outlook.coverage__target_no_qc_peps

# np.quantile(coverages, np.linspace(0,1,101))
zero_cover_raw_folders = set(outlook.Raw_File[coverages == 0])
output_path = Path("D:/projects/proteome_tools/RES/40_bad_folders")
res_path = Path(r'D:/projects/proteome_tools/RES')
fastas = {p.parent.stem:p for p in res_path.glob("pool*/*/*/*_reversed.fasta") if p.parent.stem in zero_cover_raw_folders}

DIA = pd.read_csv("J:/proteome_tools/DIA.csv").set_index('Raw_File')
x = DIA.loc[zero_cover_raw_folders]
raw_folders = dict(zip(x.index, x.path))


logging.basicConfig(filename=res_path/"40uglyPiglets.log",
                    format='PLGS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = get_logger(__name__)

troubles = []
dfs = {}
# proj = next(iter(zero_cover_raw_folders))
for proj in zero_cover_raw_folders:
    FA = fastas[proj]
    RF = raw_folders[proj]
    pool = FA.parent.parent.parent.stem
    OF = output_path/pool/proj[:5]/proj
    OK = False
    try:
        OK = plgs(raw_folder=RF,
                  out_folder=OF,
                  fastas=FA,
                  timeout_apex3d=120)
    except TimeoutExpired:
        logger.warning('Trying out higher energies.')
        try:
            OK = plgs(raw_folder=RF,
                      out_folder=OF,
                      fastas=FA,
                      timeout_apex3d=120,
                      low_energy_thr=600,
                      high_energy_thr=60)
        except Exception as e:
            logger.warning('Failed again.')
            troubles.append((p,e))
    if OK:
        try:
            dfs[proj],_ = wx2csv(OF/f"{proj}_IA_workflow.xml",
                                 OF/f"{proj}_report.csv")
        except Exception as e:
            troubles.append((p,e))
