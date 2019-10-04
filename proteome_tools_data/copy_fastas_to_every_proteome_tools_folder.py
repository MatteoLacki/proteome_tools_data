from itertools import chain
import json
from pathlib import Path
import shutil

from proteome_tools_data.file_iteration import all_res

ls = lambda p: list(p.glob('*'))
pools = {}
for f in Path('U:/Matteo/poligono').glob('pool*.json'):
    with f.open('r') as h:
        pools[f.stem] = json.load(h)

proj2fasta = {Path(p).stem: Path(f) for p,f in chain(pools['pool1'], pools['pool2'])}

proj2path = {p.stem: p for p in all_res}

# copy all fastas to existing projects
for proj, proj_path in proj2path.items():
    fasta_path = proj2fasta[proj]
    shutil.copy(str(fasta_path), str(proj_path))

