import cld3
import langid
from langdetect import detect
import fasttext
import re
#languages supported by all detectors
language_set = {"af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", "et", "fa", "fi", "fr", "gu", "he",
"hi", "hr", "hu", "id", "it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl",
"pt", "ro", "ru", "sk", "sl", "so", "sq", "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi", "zh-cn", "zh-tw"}

	
def clean(text): #cleans text of unnecessary elements
	text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
	result = ''.join(i for i in text if not i.isdigit() )
	result = result.replace('"', '')
	result = result.replace('\t',' ')
	result = result.replace('\n', '')

	return result

#classes corresponding to different detectors
class CLD3():
	def detect(text):
		prediction, confidence, isreliable, proportion = cld3.get_language(text)
		if(confidence >= 0.5):
			return prediction
		else:	 
			return cld3.get_language(clean(text))[0]

class LANGID():
	def detect(text):
		prediction, confidence = langid.classify(text)
		if(confidence >= 0):
			return prediction
		else:	 
			return langid.classify(clean(text))[0]		

class LANGDETECT():
	def detect(text):
		return detect(text)		

class FASTTEXT():
	global model
	model = fasttext.load_model('lid.176.ftz')
	def detect(text): #loading fasttext model
		prediction, confidence = model.predict(text)
		if(confidence[0] >= 0.5):
			return prediction[0][9:]
		else:	
			return model.predict(clean(text))[0][0][9:]
