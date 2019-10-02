import argparse
from pathlib import Path

from vodkas import apex3d, peptide3d, iadbs
from vodkas.fs import cp

parser = argparse.ArgumentParser(description='Process data for the Proteome Tools project.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

# # raw = Path("//MSSERVER/restoredData/proteome_tools/net/idefix/WIRD_GESICHERT/T1707/T170722_03.raw")#big
# raw = Path("C:/ms_soft/MasterOfPipelines/RAW/O1903/O190302_01.raw")#small
# temp = Path("C:/Symphony/Temp/test")#TODO: WTF if this file already existed?
# apexOutPath, apex_proc = apex3d(raw, temp, write_binary=True, capture_output=True)
# # apexOutPath = temp/(raw.stem + "_Apex3D")
# apexOutBIN = apexOutPath.with_suffix('.bin')
# pep3dOutPath, pep_proc = peptide3d(apexOutBIN, temp,
#                                    write_binary=True,
#                                    min_LEMHPlus=350.0,
#                                    capture_output=True)
# # pep3dOutPath = temp/(raw.stem + "_Pep3D_Spectrum")
# pep3dOutXML = pep3dOutPath.with_suffix('.xml')
# iadbsOutPath, iadbs_proc = iadbs(pep3dOutXML, temp, 
#                                  fasta_file="C:/Symphony/Search/wheat.fasta",
#                                  parameters_file="C:/Symphony/Search/251.xml",
#                                  capture_output=True)
