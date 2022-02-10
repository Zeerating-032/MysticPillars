# -*- coding: utf-8 -*-
'''
@Last Edit:2022.02.10
@Author:Zeerating
'''

'''
1. 先幫每一個柱子編號，從0到柱數-1
2. 輸入寶石狀態皆須按照編號輸入
'''

import queue
import copy

def set_shortest(E, t): #BFS
	visiting = queue.Queue()
	shortest = [[-1 for _ in range(t)] for _ in range(t)]
	
	for i in range(t):
		length = 0
		visiting.put(i)
		status = [-1 for _ in range(t)]
		while 1:
			temp_visit = []
			while not visiting.empty():
				p = visiting.get()
				shortest[i][p] = length
				for j in range(t):
					if E[p][j] == 1 and status[j] == -1:
						temp_visit.append(j)
						status[j] = 0

			length += 1
			while len(temp_visit) != 0:
				visiting.put(temp_visit.pop())
			status[i] = 1
			if visiting.empty():
				break
	return shortest

def canContinue(v, fini, remaining_step):
	diff = 0
	for i, j in zip(v, fini):
		if i != j:
			diff += 1
	if diff > 2*remaining_step: #一次移動只能改變兩根柱子，可依此推算是否有解
		return 0
	else:
		return 1

def canTrans(v, from_to, shortest):
	t1, t2 = from_to
	if v[t1] >= shortest[t1][t2]: #寶石足夠才能移動
		return 1
	else:
		return 0
	
def trans(v, from_to, shortest): #移動寶石
	t1, t2 = from_to
	vv = [] # 這樣記憶體不會重疊
	for i in range(len(v)):
		if i == t1:
			vv.append(v[i] - shortest[t1][t2])
		elif i == t2:
			vv.append(v[i] + shortest[t1][t2])
		else:
			vv.append(v[i])
	return vv

def solve(v, fini, remaining_step, all_trans_way, shortest, step_record=[], last_change=(-1, -1)):
	global step_stack
	if v == fini:
		output(step_record)
		return
	elif not canContinue(v, fini, remaining_step):
		return
	elif remaining_step == 0:
		return
	else:
		for i in range(len(all_trans_way)):
			if canTrans(v, all_trans_way[i], shortest) and all_trans_way[i] != (last_change[1], last_change[0]): #不能換回去
				temp_step_record = copy.deepcopy(step_record)
				temp_step_record.append(all_trans_way[i])
				solve(trans(v, all_trans_way[i], shortest), fini, remaining_step-1, all_trans_way, shortest, temp_step_record, last_change=all_trans_way[i])
		return

def output(lis):
	i = 1
	print("*************************")
	for i in range(len(lis)):
		print(f"第{i+1}步，從{lis[i][0]}到{lis[i][1]}")
	print("*************************")

t = int(input("柱子數量:"))
V = list(map(int, input("各柱子的初始寶石數:").split()))
E = [[0 for _ in range(t)] for _ in range(t)]


print("輸入有雙向道的兩根柱子編號(輸入-1 -1結束):")
while 1:
	a, b = tuple(map(int, input().split()))
	if a == b == -1:
		break
	E[a][b] = E[b][a] = 1
print("輸入有單行道的兩根柱子編號(前為起點，輸入-1 -1 結束):")
while 1:
	a, b = tuple(map(int, input().split()))
	if a == b == -1:
		break
	E[a][b] = 1

max_step = int(input("最大步數:"))
finish_V = list(map(int, input("最終目標寶石數:").split()))

shortest = set_shortest(E, t) #兩柱子間的最短距離

print("Shortest:", shortest)

all_trans_way = [] #所有可移動的起點/終點組合
for i in range(t):
	for j in range(t):
		if shortest[i][j] != -1: #沒路
			all_trans_way.append((i, j))
print("all_trans_way:", all_trans_way)

solve(V, finish_V, max_step, all_trans_way, shortest)