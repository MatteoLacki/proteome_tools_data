"""Run the pipeline for the Proteome Tools project."""
from pathlib import Path
from pprint import pprint
import json

from vodkas import apex3d, peptide3d, iadbs, wx2csv

debug = True
capture_output = True
proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
parameters_file = proj_folder/"params/515.xml"
with open(proj_folder/"plate1.json", 'r') as f:
    settings = json.load(f)

SETTINGS = {Path(s[0]).stem: s for s in settings}
RES = Path(r'D://projects/proteome_tools/RES')

recalculate = []
for proj in RES.glob('*/*'):
    if not list(proj.glob('report.csv')):
        recalculate.append(proj)

exceptions= {}
# out_folder = next(iter(recalculate))
for out_folder in recalculate:
    proj_no = out_folder.stem
    _, fastapath = SETTINGS[proj_no]
    try:
        pep3dOut = out_folder/(proj_no + "_Pep3D_Spectrum")
        iadbsOut, iadbs_proc = iadbs(pep3dOut.with_suffix('.xml'),
                                     out_folder, 
                                     fasta_file=fastapath,
                                     parameters_file=parameters_file,
                                     capture_output=capture_output,
                                     debug=debug)
        if debug:
            print(iadbsOut, iadbs_proc)
        report, wx2csv_proc = wx2csv(iadbsOut.with_suffix('.xml'),
                                     out_folder/"report.csv",
                                     debug=debug)
        if debug:
            print(report, wx2csv_proc)
            print("Finished")
    except Exception as e:
        exceptions[out_folder] = e
        print(e)


iadbsOut, iadbs_proc = iadbs(pep3dOut.with_suffix('.xml'),
                             out_folder, 
                             fasta_file=fastapath,
                             parameters_file=parameters_file,
                             capture_output=capture_output,
                             debug=debug)


input_file = pep3dOut.with_suffix('.xml')
output_dir = out_folder
fasta_file = fastapath
parameters_file = parameters_file


import vodkas.default_paths as default
path_to_iadbs=default.iadbspath

algo = Path(path_to_iadbs)
input_file = Path(input_file)
output_dir = Path(output_dir)
fasta_file = Path(fasta_file)
fasta_file = Path(str(fasta_file).replace('\\\\MSSERVER\\restoredData','J:\\'))

parameters_file = Path(parameters_file)
write_xml=True
write_binary=False
write_csv=False
import subprocess

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

if '_Pep3D_Spectrum' in input_file.stem:
    out = output_dir/input_file.stem.replace('_Pep3D_Spectrum','_IA_workflow')
else:
    out = output_dir/(input_file.stem + "_IA_workflow")
out_bin = out.with_suffix('.bin')
out_xml = out.with_suffix('.xml')
if kwds.get('capture_output', False):# otherwise no input was caught.
    log = output_dir/"iadbs.log"
    log.write_bytes(process.stdout)
if debug:
    print(out_bin, out_bin.exists())
    print(out_xml, out_xml.exists())
    print((not out_bin.exists()) or (not out_xml.exists()))
if (not out_bin.exists()) and (not out_xml.exists()):# none exists
    raise RuntimeError("WTF: output is missing: iaDBs failed.")
if process.stderr:
    print(process.stderr)
    raise RuntimeError("iaDBs failed: WTF")
if debug:
    print(out_bin.with_suffix(''))

