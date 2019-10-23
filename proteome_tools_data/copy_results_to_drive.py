"""Here we copy the raw files to the big disk."""
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from pathlib import Path
from pprint import pprint
import shutil

from vodkas.fs import copy_folder



pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)

ls = lambda p: pprint(list(p))

raw_folders = Path("E:/net/restoredData/proteome_tools/net")
raw_folders = Path("J:/proteome_tools/net")
raw_folders = {r.stem:r for r in raw_folders.glob("*/WIRD_GESICHERT/[T,S]*/[T,S]*")}

dest = Path("F:/DIA/raw")
outlook = pd.read_csv("E:/net/restoredData/proteome_tools/outlook.csv")
outlook = pd.read_csv("J:/proteome_tools/outlook.csv")
raw2pool = dict(zip(outlook.Raw_File, outlook.pool))

def copy(src_dst):
    src, dst = src_dst
    shutil.copytree(src=str(src), dst=str(dst))
    return 1

def copy2(src_dst):
    copy_folder(*src_dst)
    return 1

#r = next(iter(raw2pool))
src_dst_list = [(raw_folders[r], dest/f"pool{raw2pool[r]}/{r[:5]}/{r}.raw") for r in raw2pool]
src_dst_list = [ (r,d) for r,d in src_dst_list if "pool1\\S1803\\" not  in str(d) ]

# status = massive_copy(src_dst_list[2:])

def massive_copy(src_dst_list, threads_no=5, copy=copy2):
    with ThreadPoolExecutor(threads_no) as e:
        w = list(e.map(copy2, src_dst_list))
    return w

copy_folder(*src_dst_list[0])
status = massive_copy(src_dst_list[1:6])


from time import time

status = massive_copy(src_dst_list[6:7], 1)

T0 = time()
status = massive_copy(src_dst_list[7:12], 1)
T1 = time()
status = massive_copy(src_dst_list[12:17], 5)
T2 = time()

T1 - T0
T2 - T1

T3 = time()
status = massive_copy(src_dst_list[17:22], 2)
T4 = time()
T4 - T3
# and the winner is: one thread of robocopy! Good: simple and shows output too.

status = massive_copy(src_dst_list[22:], 1)