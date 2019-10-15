"""Some 30 projects had wrong fastas due to wrong pool being selected."""
import json
from pathlib import Path
import shutil
from furious_fastas import Fastas, fastas
from furious_fastas.fasta import NCBIgeneralFasta
from vodkas import iadbs


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

