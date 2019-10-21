from collections import Counter
from pathlib import Path
from furious_fastas import Fastas, fastas

from proteome_tools_data.coverages.coverages import find_target

res = Path(r"D:/projects/proteome_tools/RES")


# proj_folder = next(res.glob("pool*/*/*"))
def check_fasta_folders(res):
    for proj_folder in res.glob("pool*/*/*"):
        fasta_path = next(proj_folder.glob("*_reversed.fasta"))
        target = find_target(fastas(fasta_path))
        yield int(target.description.split('_')[-1]) == int(fasta_path.stem.split('_')[0])

Counter(check_fasta_folders(res))


def check_pools(res):
    for proj_folder in res.glob("pool*/*/*"):
        fasta_path = next(proj_folder.glob("*_reversed.fasta"))
        target = find_target(fastas(fasta_path))
        pool_a = {'first':1, 'second':2}[target.description.split('_')[1]]
        pool_b = int(proj_folder.parent.parent.stem[4])
        yield pool_a == pool_b

Counter(check_pools(res))


