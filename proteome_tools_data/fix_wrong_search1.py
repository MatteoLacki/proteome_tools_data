"""Some 30 projects had wrong fastas due to wrong pool being selected."""
import json
from pathlib import Path
import shutil
from furious_fastas import Fastas, fastas
from furious_fastas.fasta import NCBIgeneralFasta
from vodkas import iadbs, wx2csv
from vodkas.logging import get_logger
import logging
import pandas as pd

from proteome_tools_data.recalculate_coverages import iter_res
from proteome_tools_data.file_iteration import all_res, get_pools_proj2fasta
from proteome_tools_data.coverages.coverages import get_input_for_coverages, get_coverages

pt = Path("J:/proteome_tools")

with open(pt/"pool1fix.json", 'r') as f:
    pool1fix = json.load(f)

res_path = Path(r'D:\projects\proteome_tools\RES\pool1')

logging.basicConfig(filename=res_path.parent/"fix_pool1_fastas.log",
                    format='FIXING_FASTAS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = get_logger(__name__)

def reformulate_fasta(f):
    pack, desc = f.header.split('|')
    pack = pack[1:]
    return NCBIgeneralFasta(pack, pack, desc, f.sequence)

# raw, fasta = pool1fix[0]
for raw, fasta in pool1fix:
    # copy
    raw = Path(raw)
    fasta = Path(fasta)
    res_folder = res_path/raw.parent.stem/raw.stem
    shutil.copy(str(fasta), str(res_folder/fasta.name))
    # reversal
    FF = Fastas(reformulate_fasta(f) for f in fastas(fasta))
    FF.reverse()
    rev_fasta_path = res_folder/f"{fasta.stem}_reversed.fasta"
    FF.write(rev_fasta_path)
    # rerun iadbs
    try:
        outfile, _ = iadbs(res_folder/f"{raw.stem}_Pep3D_Spectrum.xml", 
                           res_folder/'reversed_search',
                           rev_fasta_path)
    except Exception as e:
        problems.append((str(f), repr(e)))
        logger.warning(repr(e))

# troubles = []
# # raw,_ = pool1fix[0]
# for raw,_ in pool1fix:
#     raw = Path(raw)
#     res_folder = res_path/raw.parent.stem/raw.stem
#     try:
#         df,_ = wx2csv(res_folder/'reversed_search'/f"{raw.stem}_IA_workflow.xml",
#                       res_folder/'reversed_search'/f"{raw.stem}_report.csv")
#     except Exception as e:
#         print(e)
#         troubles.append(e)

res = Path(r"D:/projects/proteome_tools/RES")

# RECALCULATING ALL THE BLOODY REPORTS
troubles = []
# proj_folder = next(res.glob("pool*/*/*"))
for proj_folder in res.glob("pool*/*/*"):
    try:
        df,_ = wx2csv(proj_folder/'reversed_search'/f"{proj_folder.stem}_IA_workflow.xml",
                      proj_folder/'reversed_search'/f"{proj_folder.stem}_report.csv")
    except Exception as e:
        print(e)
        troubles.append(e)

# proj_folder = next(res.glob("pool*/*/*"))
def iter_coverages(res):
    for proj_folder in res.glob("pool*/*/*"):
        report_path = proj_folder/"reversed_search"/f"{proj_folder.stem}_report.csv"
        fasta_path = next(proj_folder.glob("*_reversed.fasta"))
        yield get_coverages(*get_input_for_coverages(report_path, fasta_path))

outlook = pd.DataFrame(iter_coverages(res))




# compare this to the list of wanted results.
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)

DIA = pd.read_csv(pt/'DIA.csv')


with open(pt/'pool1.json'):

list(res.glob("pool*/*/*/reversed_search/*_report.csv"))

