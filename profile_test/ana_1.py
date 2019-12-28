import read as rd
import pandas
import pprint as pp


def un(a: list, b: list):
    return set(a).union(b)


def totaladd():
    a1 = rd.read("00e5c44d5a")
    a2 = rd.read("0b9a801551")
    a3 = rd.read("0c6bf1ac1e")
    a4 = rd.read("0f6400cc09")
    a5 = rd.read("1b5e66ad58")
    edname = un(a1.keys(), un(a2.keys(), un(a3.keys(), un(a4.keys(), a5.keys()))))
    val = [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]
    totalvalue = {}
    for i in edname:
        if i in a1.keys():
            val[0][0] = a1[i][0]
            val[1][0] = a1[i][1]
        if i in a2.keys():
            val[0][1] = a2[i][0]
            val[1][1] = a2[i][1]
        if i in a3.keys():
            val[0][2] = a3[i][0]
            val[1][2] = a3[i][1]
        if i in a4.keys():
            val[0][3] = a4[i][0]
            val[1][3] = a4[i][1]
        if i in a5.keys():
            val[0][4] = a5[i][0]
            val[1][4] = a5[i][1]
        totalvalue[i] = val

    return totalvalue


def difva(a: list):
    b = [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]]
    for i in range(1, 5):
        b[0][i] = a[i] - a[i - 1]
        b[1][i] = b[0][i] / a[i - 1]
    return b


def difvas(a: dict):
    name = a.keys();
    rs = {}
    for i in name:
        rs[i] = [difva(a[i][0]),difvas(a[i][1])]
    return rs


