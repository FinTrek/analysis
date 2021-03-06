# python 3 

import argparse
import os
from os import listdir
from os.path import isfile, join                                                                       
from multiprocessing import Pool                                                
       

print ('*'*70)
print (' run "python run_multi_process.py  --h" for help msg ')
print ('*'*70)



# ----------------------------------------------
# get args 
parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help='The url to load csv')
parser.add_argument('--script', required=True, help='which script want to run')
parser.add_argument('--process', required=True, help='How many processes plan to run on the same time')
args = parser.parse_args()

url  = args.url 
script  = args.script 
process  = args.process 
# ----------------------------------------------


def run_process(process):
	# python script.py --csv demp.csv                                                         
	os.system('python {}'.format(process))                                       


def collect_processes(script, url):
	sub_url = '/' + '/'.join([ i for i in url.split('/')[1:-1]]) + '/'  
	file_list = [ i for i in listdir(sub_url) if 'sub' in i ]
	csvurl =  [ sub_url + i for i in listdir(sub_url) if 'sub' in i ]
	#processes = [ '{}  --url {} --csv {}'.format(script, url, j)  for j in file_list ]
	processes = [ '{}  --csvurl {}'.format(script,j)  for j in csvurl ]

	print (' *** processes :  *** ', processes)
	return processes 

def main(num_process,processes):
	pool = Pool(processes=num_process)                                                        
	pool.map(run_process, processes)


if __name__ == '__main__':
	#num_process=5
	num_process = int(process)
	print (' *** num_process : *** ', num_process)
	processes=collect_processes(script,url)
	main(num_process,processes)


