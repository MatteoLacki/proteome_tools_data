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
def iter_results(res):
    for proj_folder in res.glob("pool*/*/*"):
        report_path = proj_folder/"reversed_search"/f"{proj_folder.stem}_report.csv"
        fasta_path = next(proj_folder.glob("*_reversed.fasta"))
        peptides, target, qcs, all_peptides_no = get_input_for_coverages(report_path, fasta_path)
        r = get_coverages(peptides, target, qcs)
        r['fasta'] = fasta_path.stem
        r['proj_no'] = proj_folder.stem
        r['pool'] = proj_folder.parent.parent.stem
        r['all_peptides_no'] = all_peptides_no
        r['filtered_peptides_no'] = len(peptides)
        yield r

outlook = pd.DataFrame(iter_results(res))
outlook = outlook.set_index('proj_no')

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)

DIA = pd.read_csv(pt/'DIA.csv')
DIA = DIA.rename(columns={'Raw_File':'proj_no'})
DIA = DIA.set_index('proj_no')

final_outlook = outlook.merge(DIA, on='proj_no')
final_outlook = final_outlook.drop(columns=['parsed_name', 'fasta_file', 'path','MS_Methode','LC_Methode',])
final_outlook = final_outlook[['Sample_Name','pool','fasta','all_peptides_no','filtered_peptides_no','JPT_QC_Peptide','JPT_RT_Peptide','PRTC_RT_Peptide','target_no_qc_peps','target_with_qc_peps']]
final_outlook = final_outlook.rename(columns={col: f"coverage__{col}" for col in final_outlook.columns[-5:]})
final_outlook.index.name = 'Raw_File'
final_outlook.pool = [int(p[4]) for p in final_outlook.pool]

# sorting for reading purposes
final_outlook = final_outlook.reset_index()

final_outlook['no'] = [int(rf.split("_")[1][:3]) for rf in final_outlook.Raw_File]
final_outlook['raw'] = [rf[:4] for rf in final_outlook.Raw_File]
final_outlook = final_outlook.sort_values(by=['pool','raw','no'])
final_outlook = final_outlook.drop(columns=['raw','no'])
final_outlook.to_csv(Path("D:/projects/proteome_tools/RES/outlook.csv"), index=False)


# debugging the search
