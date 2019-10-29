from pathlib import Path
from pprint import pprint
import pandas as pd

from proteome_tools_data.coverages.coverages import get_input_for_coverages, get_coverages

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)


res = Path(r'D:\projects\proteome_tools\RES') 
csvs = {c.stem.replace('_report',''): c
   for c in Path(res/'40_bad_folders').glob('pool*/*/*/*_report.csv')
}
fasta_paths = {p.parent.stem:p for p in res.glob("pool*/*/*/*_reversed.fasta") if p.parent.stem in projects}

DIA = pd.read_csv("J:/proteome_tools/DIA.csv").set_index('Raw_File')
rep = next(iter(csvs))
rep


def iter_reports():
    for rep in csvs:
        report_path = csvs[rep]
        fasta_path = fasta_paths[rep]
        peptides, target, qcs, all_peptides_no = get_input_for_coverages(report_path, fasta_path)
        pool = int(fasta_path.parents[2].stem[4])
        cov = get_coverages(peptides, target, qcs)
        yield rep, DIA.loc[rep].Sample_Name, pool, fasta_path.stem, all_peptides_no, len(peptides),  cov['JPT_QC_Peptide'], cov['JPT_RT_Peptide'], cov['PRTC_RT_Peptide'], cov['target_no_qc_peps'], cov['target_with_qc_peps']

R = pd.DataFrame(iter_reports())
R.columns = 'Raw_File','Sample_Name','pool','fasta','all_peptides_no','filtered_peptides_no','coverage__JPT_QC_Peptide','coverage__JPT_RT_Peptide','coverage__PRTC_RT_Peptide','coverage__target_no_qc_peps','coverage__target_with_qc_peps'
R = R.set_index('Raw_File')
R.to_csv(R/"")
