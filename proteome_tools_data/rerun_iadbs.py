from furious_fastas import fastas
from furious_fastas.fasta import NCBIgeneralFasta
from furious_fastas.fastas import Fastas
from pathlib import Path
from vodkas import iadbs
from vodkas.logging import get_logger

from proteome_tools_data.file_iteration import all_res

proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
pool2 		= Path("D:/projects/proteome_tools/RES/pool2")
parameters_file = proj_folder/"params/515.xml"

logging.basicConfig(filename=pool2/"pool2.log",
                    format='RERUN_IADBS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = get_logger(__name__)

def to_ncbi(F):
    for f in F:
        if not 'REVERSE' in f.header:
            acc, desc = f.header.split('|')
            acc = acc[1:]
            yield NCBIgeneralFasta(acc, acc, desc, f.sequence)

def reverse_fasta(fasta_file):
    F = Fastas(to_ncbi(fastas(fasta_file)))
    F.reverse()
    out_path = fasta_file.parent/f"{fasta_file.stem}_reversed.fasta"
    F.write(out_path)
    return out_path

problems = []
for p in all_res:
    fasta_file = next(f for f in p.glob('*.fasta') if not '_reversed' in str(f))
    if not fasta_file:
        print(f'Problem in {p}')
        problems.append(p)
    else:
        fasta_rev = reverse_fasta(fasta_file)

problems2 = []
for p in all_res:
	fasta_file = next(f for f in p.glob('*.fasta') if '_reversed' in str(f))
    if fasta_file:
    	iadbs_status = iadbs(input_file=p/f"{p.stem}_Pep3D_Spectrum",
    		  				 output_file=p/f"{p.stem}_IA_workflow_reversed.xml",
    		  				 fasta_file,
    		  				 parameters_file)
    else:
        problems2.append(p)