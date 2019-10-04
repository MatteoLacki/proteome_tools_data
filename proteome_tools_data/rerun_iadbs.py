from furious_fastas import fastas
from furious_fastas.fasta import NCBIgeneralFasta
from furious_fastas.fastas import Fastas
from pathlib import Path
from vodkas import iadbs
from vodkas.logging import get_logger
import logging
from shutil import copyfile
import json

from proteome_tools_data.file_iteration import all_res

proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
pool2       = Path("D:/projects/proteome_tools/RES/pool2")
parameters_file = proj_folder/"params/515.xml"

logging.basicConfig(filename=pool2/"pool2.log",
                    format='RERUN_IADBS %(asctime)s:%(name)s:%(levelname)s:%(message)s:',
                    level=logging.INFO)
logger = get_logger(__name__)

# def to_ncbi(F):
#     for f in F:
#         if not 'REVERSE' in f.header:
#             acc, desc = f.header.split('|')
#             acc = acc[1:]
#             yield NCBIgeneralFasta(acc, acc, desc, f.sequence)

# def reverse_fasta(fasta_file):
#     F = Fastas(to_ncbi(fastas(fasta_file)))
#     F.reverse()
#     out_path = fasta_file.parent/f"{fasta_file.stem}_reversed.fasta"
#     F.write(out_path)
#     return out_path

# problems = []
# for p in all_res:
#     fasta_file = next(f for f in p.glob('*.fasta') if not '_reversed' in str(f))
#     if not fasta_file:
#         print(f'Problem in {p}')
#         problems.append(p)
#     else:
#         fasta_rev = reverse_fasta(fasta_file)

# from pprint import pprint

# p = all_res[0]
# res_folders = {p.stem:p  for p in all_res}
# p = res_folders['T170722_109']

# fasta_file = next(f for f in p.glob('*.fasta') if '_reversed' in str(f))
# output_dir = p/'reversed_search'
# output_dir.mkdir(exist_ok=True)
# cmd = iadbs(input_file=p/f"{p.stem}_Pep3D_Spectrum.bin",
#                    output_dir=output_dir,
#                    fasta_file=fasta_file,
#                    parameters_file=parameters_file)
# pprint(cmd)

#  C:\SYMPHONY_VODKAS\plgs\iaDBs.exe -paraXMLFileName \\MSSERVER\restoredData\proteome_tools\params\515.xml -pep3DFileName D:\projects\proteome_tools\RES\pool1\T1707\T170722_109\T170722_109_Pep3D_Spectrum.bin -proteinFASTAFileName D:\projects\proteome_tools\RES\pool1\T1707\T170722_109\051_reversed.fasta -outputDirName D:\projects\proteome_tools\RES\pool1\T1707\T170722_109\reversed_search -WriteXML 1 -WriteBinary 1 -bDeveloperCSVOutput 0
# from subprocess import Popen, TimeoutExpired, run, PIPE

# pr = Popen(cmd, stdout=PIPE)
# out, err = pr.communicate(timeout=60)


problems2 = []
for p in all_res:
    try:
        fasta_file = next(f for f in p.glob('*.fasta') if '_reversed' in str(f))
        output_dir = p/'reversed_search'
        output_dir.mkdir(exist_ok=True)
        res_path,_ = iadbs(input_file=p/f"{p.stem}_Pep3D_Spectrum.xml",
                           output_dir=output_dir,
                           fasta_file=fasta_file,
                           parameters_file=parameters_file)
        respath = res_path.with_suffix('.xml')
        final_loc = respath.parent.parent/f"{respath.stem}_reversed.xml"
        copyfile(str(respath), str(final_loc))
    except Exception as e:
        problems2.append((p,repr(e)))

if problems2:
    with open("D:/projects/proteome_tools/RES/pool2.probs") as h:
        json.dump(problems2, h, indent=4)