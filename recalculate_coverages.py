import pandas as pd
import numpy as np
from pathlib import Path
from pep2prot.range_ops import covered_area
from pep2prot.string_ops import find_indices3
from pprint import pprint
from furious_fastas import fastas, Fastas
from itertools import chain
from collections import defaultdict
import json

from vodkas.fs import ls
ls = lambda p: list(p.glob('*'))

covered_area([(1,3), (2,6), (2,4), (10,12)])
covered_area([(1,3)])
find_indices3('AAA', 'BBAAACCCAAA')

pools = {}
for f in Path('U:/Matteo/poligono').glob('pool*.json'):
    with f.open('r') as h:
        pools[f.stem] = json.load(h)

proj2fasta = {Path(p).stem: Path(f) for p,f in chain(pools['pool1'], pools['pool2'])}
res = Path('D:/projects/proteome_tools/RES')

def all_res(res):
    for pool in ('pool1', 'pool2'):
        for f in (res/pool).glob('*'):
            if f.stem[0] in ('S','T'):
                yield from f.glob('*')

proj = 'T170807_06'
p = {Path(p).stem:Path(p) for p in all_res(res)}[proj]

def getdata(p, no_decoys=True):
    X = pd.read_csv(p/"report.csv")
    X = X[X.type.isin({'PEP_FRAG_1', 'PEP_FRAG_2', 'VAR_MOD', 'MISSING_CLEAVAGE'})]
    F = fastas(proj2fasta[p.stem])
    if no_decoys:
        F = Fastas(f for f in F if not '>Decoy' in f.header)
    concat_fasta = str(max(F, key=lambda x: len(str(x))))
    qc_fastas = [str(f) for f in F if str(f) != concat_fasta]
    return X, F, concat_fasta, qc_fastas


def is_qc(pep, qc_prot):
    return len(find_indices3(pep, qc_prot)) > 0


def covered_qc(qc_prot, qc_peps):
    A = covered_area(sorted((s,e) for qc in qc_peps 
                                  for (s,e) in find_indices3(qc, qc_prot)))
    L = len(qc_prot)
    return A/L


def get_main_coverage(Y, fasta):
    Y = Y.copy()
    Y.columns = 's', 'e'
    Y.s -= 1
    Y = Y.sort_values(by='s')
    covered = covered_area(zip(Y.s, Y.e))
    total_len = len(fasta)
    return covered/total_len


def get_coverage(report_path):
    X, F, concat_fasta, qc_fastas = getdata(report_path)
    qc_prots2peps = {qc_prot:[pep for pep in X.sequence if is_qc(pep, qc_prot)]
                              for qc_prot in qc_fastas}
    qc_peps = {pep for peps in qc_prots2peps.values() for pep in peps}
    coverages = {qc_prot: covered_qc(qc_prot, qc_peps) 
                 for qc_prot, qc_peps in qc_prots2peps.items()}
    # the other peptides
    other_peps = X[~X.sequence.isin(qc_peps)].copy()
    other_peps = other_peps[['start position', 'end position']]
    coverages['peptide_coverage'] = get_main_coverage(other_peps, concat_fasta)
    return coverages

def iter_res(res):
    for p in all_res(res):
        try:
            res = get_coverage(p)
            res['acquired_name'] = p.stem
            res['fasta'] = proj2fasta[p.stem].name
            res['pool'] = int(p.parent.parent.stem[-1])
            yield res
        except FileNotFoundError:
            print(p)
            pass

# it = iter_res(res)
RES = pd.DataFrame(iter_res(res))
RES.columns
RES.to_csv(res/'overlook.csv')

RES.to_csv()