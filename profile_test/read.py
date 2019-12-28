import pstats
import pprint
import json as js

def read(a):
    p1 = pstats.Stats("process/profile/TriFusion_" + a + "_0.prof").strip_dirs().sort_stats("name").stats  # 读入数据
    p2 = pstats.Stats("process/profile/TriFusion_" + a + "_1.prof").strip_dirs().sort_stats("name").stats  # 读入数据
    p3 = pstats.Stats("process/profile/TriFusion_" + a + "_2.prof").strip_dirs().sort_stats("name").stats  # 读入数据
    p4 = pstats.Stats("process/profile/TriFusion_" + a + "_3.prof").strip_dirs().sort_stats("name").stats  # 读入数据
    p5 = pstats.Stats("process/profile/TriFusion_" + a + "_4.prof").strip_dirs().sort_stats("name").stats  # 读入数据

    psindex = set(p1.keys()).union(set(p2.keys()).union(set(p3.keys()).union(set(p4.keys()).union(p5.keys()))))

    edtion = {}
    for i in psindex:
        num = 0;
        info = []
        info.append(0)
        info.append(0)
        if i in p1.keys():
            num += 1
            info[0] += p1[i][0]
            info[1] += p1[i][2]
        if i in p2.keys():
            num += 1
            info[0] += p2[i][0]
            info[1] += p2[i][2]
        if i in p3.keys():
            num += 1
            info[0] += p3[i][0]
            info[1] += p3[i][2]
        if i in p4.keys():
            num += 1
            info[0] += p4[i][0]
            info[1] += p4[i][2]
        if i in p5.keys():
            num += 1
            info[0] += p5[i][0]
            info[1] += p5[i][2]
        info[0] /= num
        info[1] /= num
        edtion[i] = info
    return edtion


def tofile(a: dict):
    b = []
    for i in a.keys():
        c=[i,a[i]]
        b.append(c)
    return b


if __name__ == "__main__":
    a = read("00e5c44d5a")
    pprint.pprint(a)
    ajs = js.dumps(tofile(a), indent=4)
    with open("ana.txt", "w") as fp:
        fp.write(ajs)
