from itertools import chain
import json
from pathlib import Path
import shutil

ls = lambda p: list(p.glob('*'))

pools = {}
for f in Path('U:/Matteo/poligono').glob('pool*.json'):
    with f.open('r') as h:
        pools[f.stem] = json.load(h)
proj2fasta = {Path(p).stem: Path(f) for p,f in chain(pools['pool1'], pools['pool2'])}


def all_res(res):
    for pool in ('pool1', 'pool2'):
        for f in (res/pool).glob('*'):
            if f.stem[0] in ('S','T'):
                yield from f.glob('*')

res = Path('D:/projects/proteome_tools/RES')
proj2path = {p.stem: p for p in all_res(res)}

# copy all fastas to existing projects
for proj, proj_path in proj2path.items():
    fasta_path = proj2fasta[proj]
    shutil.copy(str(fasta_path), str(proj_path))

