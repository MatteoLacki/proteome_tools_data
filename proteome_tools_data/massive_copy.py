def massive_copy(src_dst_list, threads_no=5, copy=copy2):
    with ThreadPoolExecutor(threads_no) as e:
        w = list(e.map(copy2, src_dst_list))
    return w
