from furious_fastas import fastas
from pathlib import Path
from vodkas import iadbs
from vodkas.logging import get_logger

from file_iteration import all_res, get_pools_and_proj2fastas

proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
pool2 		= Path("D:/projects/proteome_tools/RES/pool2")

parameters_file = proj_folder/"params/515.xml"

logging.basicConfig(filename=pool2/"pool2.log",
                    format='RERUN_IADBS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = get_logger(__name__)


def reverse_fasta(fasta_file):
	F = fastas(fasta_file)
	F.reverse()
	out_path = fasta_file.parent/f"{fasta_file.stem}_reversed.fasta"
	F.write(out_path)
	return out_path

for p in all_res():
	fasta_std = next(f for f in p.glob('*.fasta') if not '_reversed' in str(f))
	fasta_rev = reverse_fasta(fasta_std)
	iadbs_status = iadbs(input_file  = p/f"{p.stem}_Pep3D_Spectrum",
		  				 output_file = p/f"{p.stem}_IA_workflow",
		  				 fasta_rev,
		  				 parameters_file)