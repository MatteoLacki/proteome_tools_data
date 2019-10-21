import pandas as pd
from pathlib import Path
from furious_fastas import Fastas, fastas


def find_target(FF):
    return next(f for f in FF if 'TUM_' in f.header)

def get_input_for_coverages(report_path, fasta_path):
    X = pd.read_csv(report_path)
    all_peptides_no = len(X)
    FF = fastas(fasta_path)
    target = find_target(FF)
    qcs = [f for f in FF if not 'Reversed' in f.header and str(f) != str(target)]
    X = X[X.type.isin({'PEP_FRAG_1', 'PEP_FRAG_2', 'VAR_MOD', 'MISSING_CLEAVAGE'})]
    peptides = list(X.sequence)
    return peptides, target, qcs, all_peptides_no


def get_coverages(peptides, target, qcs):
    """Get coverages proteins with peptides."""
    qcs2peps = {qc:[s for s in peptides if s in qc] for qc in qcs}
    qc_peps = {p for ps in qcs2peps.values() for p in ps}
    coverages = {qc.description: qc.coverage(peps) for qc, peps in qcs2peps.items()}
    coverages['target_with_qc_peps'] = target.coverage(peptides)
    coverages['target_no_qc_peps'] = target.coverage(p for p in peptides if not p in qc_peps)
    return coverages
