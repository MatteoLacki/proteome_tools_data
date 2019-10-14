from pathlib import Path
from itertools import chain
import json

def all_res():
    res = Path('D:/projects/proteome_tools/RES')
    for pool in ('pool1', 'pool2'):
        for f in (res/pool).glob('*'):
            if f.stem[0] in ('S','T'):
                yield from f.glob('*')

all_res = list(all_res())


def get_pools_proj2fasta():
    pools = {}
    for f in Path('U:/Matteo/poligono').glob('pool*.json'):
        with f.open('r') as h:
            pools[f.stem] = json.load(h)
    proj2fasta = {Path(p).stem: Path(f) for p,f in chain(pools['pool1'], pools['pool2'])}
    return pools, proj2fasta

