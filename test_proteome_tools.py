"""Run the pipeline for the Proteome Tools project."""
import sys
from pathlib import Path
import json
from pprint import pprint
from multiprocessing import Pool

from vodkas import apex3d, peptide3d, iadbs, wx2csv
from vodkas.fs import cp
# prepared xml files with settings for iadbs.
# params = Path("//MSSERVER/restoredData/proteome_tools/params")
# from vodkas.iadbs import write_params_xml_file
# for min_by_per_peptide in range(2,8):
#     path = params/"{}15.xml".format(min_by_per_peptide)
#     write_params_xml_file(path = path,
#                           min_by_per_peptide=min_by_per_peptide,
#                           max_prot_mass=250000000)
debug = True
rawdatapath = sys.argv[1].encode('unicode-escape').decode()
rawdatapath = Path(rawdatapath)
if debug:
    print('rawdatapath','\n\t',rawdatapath, '\n\t',str(rawdatapath))
    print()
raw_folder  = rawdatapath.stem
temp_folder = Path("C:/Symphony/Temp/proteome_tools")/raw_folder[0:5]/raw_folder
# temp_folder = Path(r"D:/projects/proteome_tools/RAW")/raw_folder[0:5]/raw_folder
proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
final_folder= proj_folder/"RAW"/raw_folder[0:5]/raw_folder

with open(proj_folder/"test3raws.json", 'r') as f:
    settings = json.load(f)
if debug:
    pprint(settings)
    print(proj_folder)
    print(final_folder)
    print()
# apexOut, apex_proc = apex3d(rawdatapath, temp_folder,
#                                 write_binary=True,
#                                 capture_output=True,
#                                 debug=True)
# apexOutBIN = apexOut.with_suffix('.bin')
# pep3dOut, pep_proc = peptide3d(apexOutBIN, temp_folder,
#                                    write_binary=True,
#                                    min_LEMHPlus=350.0,
#                                    capture_output=True,
#                                    debug=True)
# pep3dOutXML = pep3dOut.with_suffix('.xml')
pep3dOutXML = temp_folder/(raw_folder+"_Pep3D_Spectrum.xml")
fasta_file = Path(settings[raw_folder])
if debug:
    print(pep3dOutXML, fasta_file, str(fasta_file))
for parameters_file in (proj_folder/"params").iterdir():
    if debug:
        print(parameters_file)
        print(temp_folder/parameters_file.stem)
    iadbsOut, iadbs_proc = iadbs(pep3dOutXML,
                                 temp_folder/parameters_file.stem, 
                                 fasta_file=fasta_file,
                                 parameters_file=parameters_file,
                                 capture_output=True,
                                 debug=True)
    if debug:
        print(iadbsOut, iadbs_proc)
    report, wx2csv_proc = wx2csv(iadbsOut.with_suffix('.xml'),
                                 temp_folder/parameters_file.stem/"report.csv",
                                 debug=debug)
# cp(apexOutBIN,  final_folder)
# cp(pep3dOutXML, final_folder)
# cp(iadbsOutXML, final_folder)
# cp(temp_folder/'apex3d.log', final_folder)
# cp(temp_folder/'peptide3d.log', final_folder)
# cp(temp_folder/'iadbs.log', final_folder)
#TODO: add file removal!!!!
if debug:
    print("Finished")

