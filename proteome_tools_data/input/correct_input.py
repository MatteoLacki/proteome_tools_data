"""Prepartion of files done on Linux. Execution on Windows."""
from pathlib import Path, PureWindowsPath as PWP
import pandas as pd
import json
import re
from collections import Counter
import numpy as np

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', -1)#display whole column without truncation

pt = Path("/mnt/ms/restoredData/proteome_tools")
net = pt/"net"
ms_win = Path("//MSSERVER")

def iter_raw_folders(net):
    for comp in ("idefix", "synapt"):
        yield from net.glob('{}/WIRD_GESICHERT/*/*.raw'.format(comp))

raw = pd.DataFrame({'Raw_File': p.stem,
                    'path': str(ms_win/"/".join(p.parts[3:]))
                    } for p in iter_raw_folders(net)).set_index('Raw_File')

# Sample_RAWFile_List.xlsx
srfl = pd.read_excel(pt/"automation/Sample_RAWFile_List.xlsx").iloc[:,0:4]
srfl.columns = [p.replace(' ','_') for p in srfl.columns]
srfl = srfl.set_index('Raw_File')

DDA = srfl[srfl.MS_Methode.str.contains('DDA')]
DIA = srfl[~srfl.MS_Methode.str.contains('DDA')].copy()

def pad(s, k, v='0'):
    """Pad stringv s to the left with v to match length k."""
    return v*(k-len(s)) + s

def get_fasta_file(s):
    """Get the name of the fasta file from the sample name."""
    f = s.split('-')[-1]
    return pad(f, 3) + '.fasta'

# warning: some paths are missing!!!
server_path = Path("//MSSERVER/restoredData/proteome_tools/automation")
fasta_paths = {'Pools Plate 1': server_path/"db_jorg_pool1",
               'Pools Plate 2': server_path/"db_jorg_pool1",
               'missing first Plate 2': Path(''),
               'Second Pool Plate 1': server_path/"db_jorg_pool2",
               'Second Pool Plate 2': server_path/"db_jorg_pool2",               
               'Third Pool Plate 2': Path('')}

DIA['parsed_name'] = [re.sub(' \d\d\d\d-\d\d\d-\d+','', sn).replace('TUM ','') for sn in DIA.Sample_Name]
counts = Counter(DIA.parsed_name)
DIA['fasta_file'] = [ff/f for ff, f in zip(DIA.parsed_name.map(fasta_paths),
                                           DIA.Sample_Name.apply(get_fasta_file))]
DIA = DIA.merge(raw, how='left', on='Raw_File', validate='one_to_one')

pool1_bothplates = DIA[DIA.Sample_Name.str.contains('-054-')]
pool2_bothplates = DIA[DIA.Sample_Name.str.contains('-086-')]

pool1 = list(zip(pool1_bothplates.path, (str(f) for f in pool1_bothplates.fasta_file)))
pool2 = list(zip(pool2_bothplates.path, (str(f) for f in pool2_bothplates.fasta_file)))

with open(pt/'pool1.json', 'w', encoding ="utf-8") as f:
    json.dump(pool1, f, indent=4)
with open(pt/'pool2.json', 'w', encoding ="utf-8") as f:
    json.dump(pool2, f, indent=4)

DIA.to_csv(pt/'DIA.csv')