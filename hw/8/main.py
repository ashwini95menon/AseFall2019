"""main.py"""

import csv
import random

from Col import Col 
from Num import Num
from Row import Row
from Sym import Sym
from Tbl import Tbl
from unsupTree import unsupTree
from decisionTree import decisionTree

from   copy  import deepcopy as kopy


def distance(i, j, goals):

	distance = 0
	power = 2
	count = 0
	for goal in goals:
		count += 1
		dist = None
		dist = goals[goal].dist(i.leaves[list(goals.keys()).index(goal)].mean, j.leaves[list(goals.keys()).index(goal)].mean)
		distance += dist ** power
	return distance ** (1/power) / count ** (1/power)


def dominates(i, j, goals):
	z = 0.00001
	s1, s2, n = z, z, z+len(goals)
	for goal in goals:
		a,b = i.leaves[list(goals.keys()).index(goal)].mean, j.leaves[list(goals.keys()).index(goal)].mean
		a,b = goals[goal].norm(a), goals[goal].norm(b)
		s1 -= 10**(goals[goal].weight * (a-b)/n)
		s2 -= 10**(goals[goal].weight * (b-a)/n)
	return s1/n - s2/n

def row_dominates(i, j, goals): # i and j are rows.
	z = 0.00001
	s1, s2, n = z, z, z+len(goals)
	for goal in goals:
		a,b = i[goal], j[goal]
		a,b = goals[goal].norm(a), goals[goal].norm(b)
		s1 -= 10**(goals[goal].weight * (a-b)/n)
		s2 -= 10**(goals[goal].weight * (b-a)/n)

	return s1/n - s2/n

def test_domination_predicate(tbl):

	random_rows_num = random.sample(range(1, len(tbl.rows)), 100)
	row_data = []

	for i in random_rows_num:
		row_data.append(tbl.rows[i].lst)

	tbl_goals = {}

	for g in tbl.goals:
		tbl_goals[g] = tbl.cols[g]

	dom_count = {}

	for i in range(len(row_data)):
		dom = 0
		for j in range(len(row_data)):
			if row_dominates(row_data[i], row_data[j], tbl_goals) > 0:
				dom += 1

		dom_count[i] = dom

	dom_count_sorted = sorted(dom_count.items(), key=lambda kv: kv[1])

	print(tbl.headers_text)

	for i in dom_count_sorted[:4]:
		print(row_data[i[0]], "\t best")

	print(".")
	print(".")
	print(".")
	print(".")

	for i in dom_count_sorted[-4:]:
		print(row_data[i[0]], "\t worst")

def envy_tree(me_envy, goals):

	most_envy_nodes = {}

	for i in me_envy.keys():
		dist = float('inf')
		envy_clust = None

		for j in me_envy[i]:
			distance_ = distance(i, j, goals)
			if distance_ < dist:
				min_dist = distance_
				envy_clust = j

		most_envy_nodes[i] = j

	return most_envy_nodes


def main(filename):

	inp = ""

	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			inp += ''.join(row)
			inp += "\n"

	unsupTreeobj = unsupTree(inp)
	clusters = unsupTreeobj.leaves

	goals = {}

	for g in unsupTreeobj.tbl.goals:
		goals[g] = (unsupTreeobj.tbl.cols[g])


	me_envy = {}

	for i in clusters:
		for j in clusters:
			if dominates(i, j, goals) > 0:
				if i not in me_envy:
					me_envy[i] = []
				me_envy[i].append(j)

	tbl = Tbl(1)
	tbl.readData(inp)
	test_domination_predicate(tbl)
	most_envy_nodes = envy_tree(me_envy, goals)

	for key in most_envy_nodes:

		print("--------------------------------Tree--------------------------------------")

		tbl1 = Tbl(1)

		cols = key.tbl.headers_text

		cols.append('!$new_class')
		tbl1.addcol(cols)


		for row in key.tbl.rows:
			cells = kopy(row.lst)
			cells.append(0)
			tbl1.addrow(cells)

		for row in most_envy_nodes[key].tbl.rows:
			cells = kopy(row.lst)
			cells.append(1)
			if len(cells) > len(cols):
				cells = cells[0:len(cols)]
			tbl1.addrow(cells)

		dt = decisionTree()

		tree = dt.tree(tbl1, len(tbl1.cols)-1, "Num")

		dt.showt(tree)

main('auto.csv')