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

net = Path("/mnt/ms/restoredData/proteome_tools/net/")
ms_win = Path("//MSSERVER")

def iter_raw_folders(net):
	for comp in ("idefix", "synapt"):
		yield from net.glob('{}/WIRD_GESICHERT/*/*.raw'.format(comp))

res = pd.DataFrame({'Raw_File': p.stem,
                    'path': str(ms_win/"/".join(p.parts[3:]))
                    } for p in iter_raw_folders(net))

# project description
data_on_project = Path('/home/matteo/Projects/proteome_tools')

plates = pd.read_excel(data_on_project/"Sample_RAWFile_List.xlsx")
plates.columns = [p.replace(' ','_') for p in plates.columns]
plates = plates.iloc[:,0:4]
DDA = plates[plates.MS_Methode.str.contains('DDA')]
DIA = plates[~plates.MS_Methode.str.contains('DDA')].copy()

def pad(s, k, v='0'):
	"""Pad stringv s to the left with v to match length k."""
	return v*(k-len(s)) + s

def get_fasta_file(s):
	"""Get the name of the fasta file from the sample name."""
	f = s.split('-')[-1]
	return pad(f, 3) + '.fasta'

fastas_pool_1 = ms_win/"restoredData/proteome_tools/automation/db_jorg_pool1"
fastas_pool_2 = ms_win/"restoredData/proteome_tools/automation/db_jorg_pool2"
fasta_paths = {'Pools Plate 1': fastas_pool_1,
               'Pools Plate 2': fastas_pool_2, # ERROR???
               'missing first Plate 2': Path(''),
               'Second Pool Plate 1': ms_win/"restoredData/proteome_tools/automation/db_jorg_pool2",
               'Second Pool Plate 2': ms_win/"restoredData/proteome_tools/automation/db_jorg_pool2",               
               'Third Pool Plate 2': Path('')}

fasta_paths_good = {'Pools Plate 1': fastas_pool_1,
               'Pools Plate 2': fastas_pool_1,
               'missing first Plate 2': Path(''),
               'Second Pool Plate 1': ms_win/"restoredData/proteome_tools/automation/db_jorg_pool2",
               'Second Pool Plate 2': ms_win/"restoredData/proteome_tools/automation/db_jorg_pool2",               
               'Third Pool Plate 2': Path('')}

DIA['parsed_name'] = [re.sub(' \d\d\d\d-\d\d\d-\d+','', sn).replace('TUM ','') for sn in DIA.Sample_Name]
counts = Counter(DIA.parsed_name)
DIA['fasta_file'] = DIA.Sample_Name.apply(get_fasta_file)
DIA['fasta_fold'] = DIA.parsed_name.map(fasta_paths)
DIA['fasta_file'] = [ff/f for ff, f in zip(DIA.fasta_fold, DIA.fasta_file)]

DIA['fasta_fold_good'] = DIA.parsed_name.map(fasta_paths_good)
DIA['fasta_file_good'] = [ff/f for ff, f in zip(DIA.fasta_fold_good, DIA.Sample_Name.apply(get_fasta_file))]

DIA = DIA.merge(res, 'left', validate='one_to_one')
DIA['top_fold'] = [Path(p).parent.name + '/' + Path(p).name for p in DIA.path]
DIA = DIA.set_index('Raw_File')

pool1_bothplates = DIA[DIA.Sample_Name.str.contains('-054-')]
pool2_bothplates = DIA[DIA.Sample_Name.str.contains('-086-')]
all(pool1_bothplates.fasta_file == pool1_bothplates.fasta_file_good)
all(pool2_bothplates.fasta_file == pool2_bothplates.fasta_file_good)

wrong = np.array(pool1_bothplates.index)[(pool1_bothplates.fasta_file == pool1_bothplates.fasta_file_good).values]




set(pool1_bothplates.fasta_fold.map(lambda p: p.name))
db2 = set(p.name for p in Path("/mnt/ms/restoredData/proteome_tools/automation/db_jorg_pool2").glob("*.fasta"))
assert all(p.name in db2 for p in pool2_bothplates.fasta_file), "Some fasta files are missing."


# COMPARING WITH THE OLD LIST
# with (data_on_project/'plate1.json').open('r', encoding ="utf-8") as f:
#     plate1 = json.load(f)

# analysed = {Path(p).stem for p,f in plate1}
# A = plates.loc[analysed]
# A_ok = A[A.Sample_Name.str.contains('-054-')]
# '127' in {Path(f).stem for f in A_ok.fasta_file}

# with (data_on_project/'good_files.json').open('w', encoding ="utf-8") as f:
#     json.dump(list(A_ok.top_fold), f, indent=2)


pool1 = list(zip(pool1_bothplates.path, (str(f) for f in pool1_bothplates.fasta_file)))
pool2 = list(zip(pool2_bothplates.path, (str(f) for f in pool2_bothplates.fasta_file)))

with (data_on_project/'pool1.json').open('w', encoding ="utf-8") as f:
    json.dump(pool1, f, indent=4)
with (data_on_project/'pool2.json').open('w', encoding ="utf-8") as f:
    json.dump(pool2, f, indent=4)


net_folder = Path('/mnt/ms/users/Matteo/poligono')

# {Path(p).stem for p,f in pool2 if Path(p).stem[0] == 'S'}
# copy fasta files to the existing folders

