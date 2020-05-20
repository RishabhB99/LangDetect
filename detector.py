import sys
from utilities import *


def accuracy(input_set,output_set,dataset_size,check,detector):
	correct=0
	total=0.0
	for itr in range(dataset_size):
		if(check):
			if(output_set[itr] in language_set):
				if(detector.detect(input_set[itr])==output_set[itr]):
					correct+=1
				total+=1
		else:
			if(detector.detect(input_set[itr])==output_set[itr]):
				correct+=1
			total+=1

	return correct/total	

def command(argument):
	global input_set,output_set,dataset_size
	global check

	if(argument=="--help"):
		print("There is option to test 4 language detectors namely cld3, langid, langdetect and fasttext\n")
		print("Please add arguments in the following order:")
		print("1. To specify input dataset add argument --input=input_file")
		print("2. To specify output dataset add argument --output=output_file (Make sure your output dataset is in ISO 639-1 codes)")
		print("3. To specify dataset size add argument --size=dataset_size")
		print("4. If you don't want to limit the languages used by the detectors add argument --check=false")
		print("5. To test a language detector add correspoding argument: --cld3, --langid, --langdetect and --fasttext")

	if(argument[:7]=="--input"):
		file = open(argument[8:],"r")
		with file as inp:
			input_set = inp.readlines()

		for i in range(len(input_set)):
			input_set[i]=input_set[i].rstrip("\n")
				
		check = 1 	

	if(argument[:8]=="--output"):
		file = open(argument[9:],"r")
		with file as out:
			output_set = out.readlines()

		for i in range(len(output_set)):
			output_set[i]=output_set[i].rstrip("\n")
	
	if(argument[:6]=="--size"):
		dataset_size = int(argument[7:])

	if(argument=="--check=false"):
		check=0	

	if(argument=="--cld3"):
		print("CLD3 accuracy = ",accuracy(input_set,output_set,dataset_size,check,CLD3))	

	if(argument=="--langid"):
		print("LANGID accuracy = ",accuracy(input_set,output_set,dataset_size,check,LANGID))	
	
	if(argument=="--langdetect"):
		print("LANGDETECT accuracy = ",accuracy(input_set,output_set,dataset_size,check,LANGDETECT))	

	if(argument=="--fasttext"):
		print("FASTTEXT accuracy = ",accuracy(input_set,output_set,dataset_size,check,FASTTEXT))	


def main():
	for i in range(1,len(sys.argv)):
		command(sys.argv[i])	


main()