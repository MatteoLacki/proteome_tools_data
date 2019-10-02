"""Run the pipeline for the Proteome Tools project."""
from pathlib import Path
from pprint import pprint
import json
from collections import defaultdict
import subprocess
from time import time

from vodkas import apex3d, StdErr, peptide3d, iadbs, wx2csv

debug = True
capture_output = True
timeout = 60*60*24 # seconds
proj_folder = Path(r"//MSSERVER/restoredData/proteome_tools")
parameters_file = proj_folder/"params/515.xml"
with open(proj_folder/"pool2.json", 'r') as f:
    settings = json.load(f)

if debug:
    print('Tasks:')
    pprint(settings)
    print()


exceptions = defaultdict(list)


# rawdatapath, fastapath = settings[2]
# data = settings[2:3]
# data = settings[2:]
# data = settings[3:]
# data = [(a,b) for a,b in settings if 'T170825_60' in a]
# rawdatapath, fastapath = data[0]
T1708_folder = Path("D:/projects/proteome_tools/RES/pool2/T1708")
analysed = {p.name for p in T1708_folder.glob("*")}
"T170825_60" in analysed
data = [(r,f) for r,f in settings if Path(r).stem not in analysed]
assert {Path(r).stem for r,f in data}.intersection(analysed) == set([])
# rawdatapath, fastapath = data[0]
# data = [data[0]]
timings = {}

for rawdatapath, fastapath in data:
    OK = True
    rawdatapath= Path(rawdatapath)
    fastapath  = Path(fastapath)
    raw_folder = rawdatapath.stem
    out_folder = Path("D:/projects/proteome_tools/RES/pool2")/raw_folder[0:5]/raw_folder
    if debug:
        print('rawdatapath', '\n\t', rawdatapath, '\n\t', str(rawdatapath))
        print('fastapath', '\n\t', fastapath, '\n\t', str(fastapath))
        print('raw_folder', '\n\t', raw_folder)
        print('out_folder', '\n\t', out_folder)
        print('parameters_file','\n\t', parameters_file)
        print('timeout\n\t{} h'.format(timeout/3600))
    timings[raw_folder] = {}
    try:
        t_apex = time()
        apexOut, apex_proc = apex3d(rawdatapath,
                                    out_folder,
                                    write_binary=True,
                                    capture_output=capture_output,
                                    debug=debug,
                                    timeout=timeout)
        timings[raw_folder]['apex3d'] = t_apex = time() - t_apex
        if debug:
            print(apexOut, apex_proc)
    except subprocess.TimeoutExpired:
        print("apex3d reached a timeout of {} hour(s).".format(timeout/3600))
        OK = False
    except StdErr as e:
        print("Sometimes the errors are not reflected in the output.")
        print(e.err)
        apexOut = out_folder/(out_folder.name + "_Apex3D.bin")
        exceptions[rawdatapath].append(e)
        OK = False
    if OK:
        try:
            t_pep3d = time()
            pep3dOut, pep_proc = peptide3d(apexOut.with_suffix('.bin'),
                                           out_folder,
                                           write_binary=True,
                                           min_LEMHPlus=350.0,
                                           capture_output=capture_output,
                                           debug=debug)
            timings[raw_folder]['peptide3d'] = t_pep3d = time() - t_pep3d
            if debug:
                print(pep3dOut, pep_proc)
        except Exception as e:
            print(e)
            OK = False
            exceptions[rawdatapath].append(e)
        except subprocess.TimeoutExpired:
            print("pep3d reached a timeout of {} hour(s).".format(timeout/3600))
            OK = False
    if OK:
        try:
            t_iadbs = time()
            iadbsOut, iadbs_proc = iadbs(pep3dOut.with_suffix('.xml'),
                                         out_folder, 
                                         fasta_file=fastapath,
                                         parameters_file=parameters_file,
                                         capture_output=capture_output,
                                         debug=debug)
            timings[raw_folder]['iadbs'] = t_iadbs = time() - t_iadbs
            if debug:
                print(iadbsOut, iadbs_proc)
        except Exception as e:
            print(e)
            exceptions[rawdatapath].append(e)
            OK = False
        except subprocess.TimeoutExpired:
            print("iadbs reached a timeout of {} hour(s).".format(timeout/3600))
            OK = False
    # iadbsOut = Path(r"D:/projects/proteome_tools/RES/T1707/T170722_03/T170722_03_IA_workflow")
    # out_folder= Path(r"D:/projects/proteome_tools/RES/T1707/T170722_03")
    if OK:
        try:
            t_wx2csv = time()
            report, wx2csv_proc = wx2csv(iadbsOut.with_suffix('.xml'),
                                         out_folder/"report.csv",
                                         debug=debug)
            timings[raw_folder]['wx2csv'] = t_wx2csv = time() - t_wx2csv
            if debug:
                print(report, wx2csv_proc)
                print("Finished")
        except Exception as e:
            print(e)
            exceptions.append(e)

timings_path = Path("D:/projects/proteome_tools/RES/pool2/timings.json")
with open(timings_path, 'w') as f:
    json.dump(timings, f, indent=4)

print("And now all the exceptions:")
print(exceptions)