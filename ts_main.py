﻿# standard Vizard library
import viz
# infodump mode
import vizinfo
# planes and shapes
from random import shuffle
import os.path
from ts_tex import loadscene
#import ts_wid
#import ts_fri
#import ts_inc

trials = 5
savepath = "C:\Users\Cyan\Documents\\"
subjid = raw_input("Enter participant ID: ")
flname = savepath + "test_subj" + subjid + ".txt"
results = open(flname, "a")

		
"""conds = ["00", "01", "02", "03", "04", "05", "10", "11", "12", "13", "14", "15", "20", "21", "30", "31"]
shuffle(conds)
i = 0
for c in conds:
	print str(c[0]) + "," + str(c[1])
	if c[0] == "0":
		tex = int(c[1])
		loadscene(tex)if __name__ == '__main__':
	#pathcond = randint(0,2)
	pathcond = 3
	if pathcond == 0:
		gentex = randint(0,5)
		gentex = 5
		ts_tex.loadscene(trials, gentex)
	elif pathcond == 1:
		genwid = randint(0,5)
		genwid = 4
		ts_wid.loadscene(trials, genwid)
	elif pathcond == 2:
		genfri = randint(0,1)
		genfri = 0
		ts_fri.loadscene(trials,genfri)
	elif pathcond == 3:
		geninc = randint(0,1)
		geninc = 1
		ts_inc.loadscene(trials,geninc)
	
def getData(choice, finish_time):
	global results
	results.write("\n" + choice + "," + str(finish_time))
	
def runTrials(remaining_trials):
	remaining_trials -= 1
	print remaining_trials
	if remaining_trials != 0:
		pathcond = randint(0,2)
		if pathcond == 0:
			gentex = randint(0,5)
			ts_tex.loadscene(trials, gentex)
		elif pathcond == 1:
			genwid = randint(0,5)
			ts_wid.loadscene(trials, genwid)
		elif pathcond == 2:
			genfri = randint(0,1)
			ts_fri.loadscene(trials,genfri)
		elif pathcond == 3:
			geninc = randint(0,5)
			ts_inc.loadscene(trials,geninc)
	else:
		results.close()
		viz.quit()"""
		