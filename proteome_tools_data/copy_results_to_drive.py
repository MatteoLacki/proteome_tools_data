"""Here we copy the raw files to the big disk."""
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from pathlib import Path
from pprint import pprint
import shutil

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 100)

ls = lambda p: pprint(list(p))

raw_folders = Path("E:/net/restoredData/proteome_tools/net")
raw_folders = {r.stem:r for r in raw_folders.glob("*/WIRD_GESICHERT/[T,S]*/[T,S]*")}

dest = Path("F:/DIA/raw")

outlook = pd.read_csv("E:/net/restoredData/proteome_tools/outlook.csv")
raw2pool = dict(zip(outlook.Raw_File, outlook.pool))


def copy(src_dst):
    src, dst = src_dst
    shutil.copytree(src=str(src), dst=str(dst))
    return 1


test_source = Path("D:/net/users/Matteo/CodeTests/Aha/gua.txt")
test_source = Path("D:/net/users/Matteo/CodeTests")
test_target = Path("F:/DIA/CodeTests")
copy((test_source, test_target))
x = [(test_source, Path("F:/DIA/CodeTests1")),
     (test_source, Path("F:/DIA/CodeTests2"))]

#r = next(iter(raw2pool))
src_dst_list = [(raw_folders[r], dest/f"pool{raw2pool[r]}/{r[:5]}/{r}")
                for r in raw2pool]


def massive_copy(src_dst_list):
    with ThreadPoolExecutor(15) as e:
        w = list(e.map(copy, src_dst_list))
    return w

status = massive_copy(src_dst_list[:2])
status = massive_copy(src_dst_list[2:])
