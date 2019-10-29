"""Here we copy the raw files to the big disk."""
import pandas as pd
from pathlib import Path
from pprint import pprint

from vodkas.fs import copy_folder

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)

ls = lambda p: pprint(list(p))

raw_folders = Path("E:/net/restoredData/proteome_tools/net")
raw_folders = Path("J:/proteome_tools/net")
raw_folders = {r.stem:r for r in raw_folders.glob("*/WIRD_GESICHERT/[T,S]*/[T,S]*")}

dest = Path("F:/DIA/raw")
# outlook = pd.read_csv("E:/net/restoredData/proteome_tools/outlook.csv")
outlook = pd.read_csv("J:/proteome_tools/outlook.csv")
raw2pool = dict(zip(outlook.Raw_File, outlook.pool))

#r = next(iter(raw2pool))
src_dst_list = [(raw_folders[r], dest/f"pool{raw2pool[r]}/{r[:5]}/{r}.raw") for r in raw2pool]
src_dst_list = [ (r,d) for r,d in src_dst_list if "pool1\\S1803\\" not  in str(d) ]

troubles = []
# source, target = src_dst_list[0]
for source, target in src_dst_list:
    try:
        copy_folder(source, target)
    except Exception as e:
        troubles.append((source, target, e))
# simple linear copy is fastes

