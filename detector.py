import cld3
import langid
import csv
from langdetect import detect
import fasttext
import sys
import re


#languages supported by all detectors
language_set = {"af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "fi", "fr", "gu", "he",
"hi", "hr", "hu", "id", "it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl",
"pt", "ro", "ru", "sk", "sl", "so", "sq", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi", "zh-cn", "zh-tw"}


def cld3accuracy(input_set,output_set,dataset_size,check):
	correct=0
	total=0.0
	for itr in range(dataset_size):
		if(check):
			if(output_set[itr] in language_set):
				if(cld3.get_language(input_set[itr])[0]==output_set[itr]):
					correct+=1
				total+=1
		else:		
			if(cld3.get_language(input_set[itr])[0]==output_set[itr]):
				correct+=1
			total+=1		

	return correct/total		


def langidaccuracy(input_set,output_set,dataset_size,check):
	correct=0
	total=0.0
	for itr in range(dataset_size):
		if(check):
			if(output_set[itr] in language_set):	
				if(langid.classify(input_set[itr])[0]==output_set[itr]):
					correct+=1
				total+=1
		else:	
			if(langid.classify(input_set[itr])[0]==output_set[itr]):
				correct+=1
			total+=1
						
	return correct/total


def langdetectaccuracy(input_set,output_set,dataset_size,check):
	correct=0
	total=0.0
	for itr in range(dataset_size):
		if(check):
			if(output_set[itr] in language_set):	
				if(detect(input_set[itr])==output_set[itr]):
					correct+=1
				total+=1
		else:	
			if(detect(input_set[itr])==output_set[itr]):
				correct+=1
			total+=1

	return correct/total


def fasttextaccuracy(input_set,output_set,dataset_size,check,model):
	correct=0
	total=0.0
	for itr in range(dataset_size):
		if(check):
			if(output_set[itr] in language_set):
				lb,acc=model.predict(input_set[itr])
				if(lb[0][9:]==output_set[itr]):
					correct+=1
				total+=1
		else:
			lb,acc=model.predict(input_set[itr])
			if(lb[0][9:]==output_set[itr]):
				correct+=1
			total+=1

	return correct/total	

def clean(text):
	text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	result = ''.join(i for i in text if not i.isdigit() )
	result = result.replace('"', '')
	result = result.replace('\t',' ')
	result = result.replace('\n', '')

	return result

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
			input_set[i]=clean(input_set[i])

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
		print("CLD3 accuracy = ",cld3accuracy(input_set,output_set,dataset_size,check))	

	if(argument=="--langid"):
		print("LANGID accuracy = ",langidaccuracy(input_set,output_set,dataset_size,check))
	
	if(argument=="--langdetect"):
		print("LANGDETECT accuracy = ",langdetectaccuracy(input_set,output_set,dataset_size,check))

	if(argument=="--fasttext"):
		model = fasttext.load_model('lid.176.ftz') #loading fasttext model
		print("FASTTEXT accuracy = ",fasttextaccuracy(input_set,output_set,dataset_size,check,model))	




for i in range(1,len(sys.argv)):
	command(sys.argv[i])	
