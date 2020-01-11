"""Tbl.py"""

import re

from Col import Col
from Num import Num
from Row import Row
from Sym import Sym

class Tbl():

    def __init__(self, oid):
        self.oid = oid
        self.rows = []
        self.cols = []
        self.xs = []
        self.ignore_index = []
        self.list_num = []
        self.headers = []
        self.headers_text = []
        self.classes = []
        self.count_tbl = 0

    def read(self, file):
        return self.__fromString(file)


    def __compiler(self, x):
        "return something that can compile strings of type x"
        try:
            if x == '?':
                return str(x)
            int(x);
            return  int(x)
        except:
            try: float(x); return  float(x)
            except ValueError:
                return str(x)

    def __string(self, s):
        "read lines from a string"
        for line in s.splitlines():
            yield line

    def __rows(self, src, sep = ",", doomed = r'([\n\t\r ]|#.*)'):
        "convert lines into lists, killing whitespace and comments"
        for line in src:
            line = line.strip()
            line = re.sub(doomed, '', line)
            if line:
                yield line.split(sep)

    def __cells(self, src):
        "convert strings into their right types"
        drop_col = []
        length = 0
        for n,cells in enumerate(src):
            if n == 0:
                length = len(cells)
                yield cells
            else:
                rows = [self.__compiler(cell) for cell in cells]
                for i in drop_col:
                    del rows[i]
                if len(rows) < length:
                    yield "Skippimg line " + str((n + 1))
                else:
                    yield rows

    def __fromString(self, s):
        "putting it all together"
        for lst in self.__cells(self.__rows(self.__string(s))):
            yield lst

    def readData(self, file):

        data = list(self.read(file))


        headers = data[0]

        data = sorted(data[1:],key=lambda x: (x[0]))

        data = [headers] + data

        for i in range(len(data)):
            row = data[i]
            if isinstance(row, list):
                if i == 0:
                    for j in range(len(row)):
                        # print(row[j][0])
                        if row[j][0] != "?":

                            self.headers.append(j)
                            self.headers_text.append(row[j])

                            if row[j][0] not in "<>!":
                                self.xs.append(j)

                            if row[j][0] in "<>$":
                                # self.list_num.append(j)
                                # self.cols.append(Num(self.count_tbl, j + 1, row[j], 0, 0, 0))
                                self.list_num.append(j)
                                if row[j][0] in "<":
                                    self.cols.append(Num(self.count_tbl, j + 1, row[j], 0, 0, 0))
                                else:
                                    self.cols.append(Num(self.count_tbl, j + 1, row[j], 0, 0, 0))
                            else:
                                self.cols.append(Sym(self.count_tbl, j + 1, row[j]))

                            self.count_tbl += 1
                        else:
                            # print(j)
                            self.ignore_index.append(j)


                else:
                    row_for_tbl = []
                    # self.n += 1
                    row_class = row[-1]

                    for j in range(len(row)):

                        if j not in set(self.ignore_index):

                            row_for_tbl.append(row[j])

                            if row[j] == '?':
                                row[j] = self.cols[j].mean

                            if j in set(self.list_num):

                                self.cols[self.headers.index(j)].addToNum(row[j])
                                self.cols[self.headers.index(j)].updateMeanAndSdAdd(row[j])
                                # self.things[row_class].cols[self.headers.index(j)].addToNum(row[j])
                                # self.things[row_class].cols[self.headers.index(j)].updateMeanAndSdAdd(row[j])

                            else:

                                self.cols[self.headers.index(j)].addSym(row[j])
                                # self.things[row_class].cols[self.headers.index(j)].addSym(row[j])

                    self.rows.append(Row(self.count_tbl, row_for_tbl))
                    if row_class not in self.classes:
                        self.classes.append(row_class)
                    # self.things[row_class].rows.append(Row(self.count_tbl, row_for_tbl))c
                    self.count_tbl+= 1

    def addcol(self,data):


        row=data


        for j in range(len(row)):

            if row[j][0] != "?":

                self.headers.append(j)
                self.headers_text.append(row[j])

                if row[j][0] not in "<>!":
                    self.xs.append(j)

                if row[j][0] in "<>$":
                    self.list_num.append(j)
                    if row[j][0] in "<":
                        self.cols.append(Num(self.count_tbl, j + 1, row[j], 0, 0, 0))
                    else:
                        self.cols.append(Num(self.count_tbl, j + 1, row[j], 0, 0, 0))
                else:
                    self.cols.append(Sym(self.count_tbl, j + 1, row[j]))

                self.count_tbl += 1
            else:
                self.ignore_index.append(j)


    def addrow(self,data):

        row = data

        row_for_tbl = []

        row_class = row[-1]

        for j in range(len(row)):

                    if j not in set(self.ignore_index):

                        row_for_tbl.append(row[j])

                        if row[j] == '?':
                            row[j] = self.cols[j].mean

                        if j in set(self.list_num):

                            self.cols[self.headers.index(j)].addToNum(row[j])
                            self.cols[self.headers.index(j)].updateMeanAndSdAdd(row[j])
                            # self.things[row_class].cols[self.headers.index(j)].addToNum(row[j])
                            # self.things[row_class].cols[self.headers.index(j)].updateMeanAndSdAdd(row[j])

                        else:

                            self.cols[self.headers.index(j)].addSym(row[j])
                            # self.things[row_class].cols[self.headers.index(j)].addSym(row[j])

        self.rows.append(Row(self.count_tbl, row_for_tbl))
        if row_class not in self.classes:
                    self.classes.append(row_class)
                # self.things[row_class].rows.append(Row(self.count_tbl, row_for_tbl))c
        self.count_tbl += 1