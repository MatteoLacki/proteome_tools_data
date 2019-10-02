from pathlib import Path
import subprocess

import vodkas.default_paths as default

algo = Path(default.iadbspath)
input_file = Path("C:/Symphony/Temp/proteome_tools/T1707/T170722_03/T170722_03_Pep3D_Spectrum.xml")
output_dir = Path("C:/Symphony/Temp/proteome_tools/T1707/T170722_03/215")
fasta_file = Path("//MSSERVER/restoredData/proteome_tools/automation/db_jorg_pool1/001.fasta")
parameters_file = Path("//MSSERVER/restoredData/proteome_tools/params/215.xml")

write_xml = True
write_binary = True
write_csv = True
debug = True

cmd = [ "powershell.exe",
        str(algo),
        "-paraXMLFileName {}".format(parameters_file),
        "-pep3DFilename {}".format(input_file),
        "-proteinFASTAFileName {}".format(fasta_file),
        "-outputDirName {}".format(output_dir),
        "-WriteXML {}".format(int(write_xml)),
        "-WriteBinary {}".format(int(write_binary)),
        "-bDeveloperCSVOutput {}".format(int(write_csv)) ]
if debug:
    print('iaDBs debug:')
    print(cmd)
process = subprocess.run(cmd)



for parameters_file in (proj_folder/"params").iterdir():
    if debug:
        print(parameters_file)
        print(temp_folder/parameters_file.stem)
    iadbsOutXML, iadbs_proc = iadbs(pep3dOutXML,
                                    temp_folder/parameters_file.stem, 
                                    fasta_file=fasta_file,
                                    parameters_file=parameters_file,
                                    capture_output=True,
                                    debug=True)
    print(iadbs_proc)



