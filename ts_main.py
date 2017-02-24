# standard Vizard library
import viz
# proximity sensing library
import vizproximity
# 'quests' library
import viztask
# infodump mode
import vizinfo
# planes and shapes
import vizshape
# lighting effects
import vizfx
from random import randint, sample
import os.path
import ts_tex
import ts_wid
import ts_fri
import ts_inc

trials = 5
savepath = "C:\Users\Cyan\Documents\\"
subjid = raw_input("Enter participant ID: ")
flname = savepath + "test_subj" + subjid + ".txt"
global results
results = open(flname, "a")

if __name__ == '__main__':
	#pathcond = randint(0,2)
	pathcond = 3
	if pathcond == 0:
		gentex = randint(0,5)
		gentex = 5
		ts_tex.loadscene(trials, gentex)
	elif pathcond == 1:
		genwid = randint(0,5)
		genwid = 5
		ts_wid.loadscene(trials, genwid)
	elif pathcond == 2:
		genfri = randint(0,1)
		genfri = 0
		ts_fri.loadscene(trials,genfri)
	elif pathcond == 3:
		geninc = randint(0,1)
		geninc = 0
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
		viz.quit()
		