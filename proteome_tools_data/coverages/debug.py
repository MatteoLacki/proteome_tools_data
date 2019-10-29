from collections import Counter
from pathlib import Path
from pprint import pprint as print
import pandas as pd
from furious_fastas import Fastas, fastas

from proteome_tools_data.coverages.coverages import get_input_for_coverages, get_coverages

res = Path(r"D:/projects/proteome_tools/RES/pool2/T1708/T170812_14")
pprint(list(res.glob('*')))

report_path = res/"reversed_search"/"T170812_14_report.csv"
fasta_path = res/"007_reversed.fasta"

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)


X = pd.read_csv(report_path)
FF = fastas(fasta_path)

target = max(FF, key=lambda x: len(str(x))) # this might be the reversed thing, too.

Counter(s in target.sequence for s in set(X.sequence))

"FFLT" in target.sequence
"PEPTIDE" in target.sequence
list(target.where_is("PEPTIDE"))
target.coverage(["PEPTIDE"]) * len(target.sequence)

qcs = [f for f in FF if not 'Reversed' in f.header and str(f) != str(target)]
X = X[X.type.isin({'PEP_FRAG_1', 'PEP_FRAG_2', 'VAR_MOD', 'MISSING_CLEAVAGE'})]
peptides = list(X.sequence)


qcs2peps = {qc:[s for s in peptides if s in qc] for qc in qcs}
qc_peps = {p for ps in qcs2peps.values() for p in ps}
coverages = {qc.description: qc.coverage(peps) for qc, peps in qcs2peps.items()}
coverages['target_with_qc_peps'] = target.coverage(peptides)
coverages['target_no_qc_peps'] = target.coverage(p for p in peptides if not p in qc_peps)