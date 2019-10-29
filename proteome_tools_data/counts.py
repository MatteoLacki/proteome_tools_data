from pathlib import Path
import pandas as pd

RES = Path("D:\projects\proteome_tools\RES")
res = list(RES.glob("pool*/[S,T]*/[S,T]*"))
len(res)
projects = {p.stem for p in res}
DIA = pd.read_csv("J:/proteome_tools/DIA.csv").set_index('Raw_File')

pd.set_option('display.max_rows', 100)
DIA[~DIA.index.isin(projects)]

raw_folders = Path("J:/proteome_tools/net")
raw_folders = {r.stem:r for r in raw_folders.glob("*/WIRD_GESICHERT/[T,S]*/[T,S]*")}

outlook = pd.read_csv(Path("D:/projects/proteome_tools/RES/outlook.csv"))
coverages = outlook.coverage__target_no_qc_peps
zero_cover_raw_folders = set(outlook.Raw_File[coverages == 0])


