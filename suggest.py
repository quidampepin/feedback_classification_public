#this script creates a local web app that can assign a tag to new feedback text

#import libraries
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/suggestCategory')

def suggest():
	#import libraries
	import requests
	import pandas as pd
	import nltk
	from nltk.stem.snowball import SnowballStemmer
	import re
	import sys
	import warnings
	import pickle


	#get language to use
	lang = request.args.get('lang')

	#get which model to use
	section = request.args.get('section')

	#process to follow if French
	if lang == 'fr':

		#function to import pickle file
		def deserialize(file):
			with open(file, 'rb') as f:
				return pickle.load(f)

		#import French training model
		model_fr = deserialize('data/model_fr.pickle')

		#return empty string if model doesn't exist
		if section not in model_fr:
			tag_str = ''

		else:
			#get the text from the feedback
			sen_fr = request.args.get('text')

			#pre-process feedback the same way as the trained feedback
			if not sys.warnoptions:
				warnings.simplefilter("ignore")

			#function to clean the word of any punctuation or special characters
			def cleanPunc(sentence):
				cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
				cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
				cleaned = cleaned.strip()
				cleaned = cleaned.replace("\n"," ")
				return cleaned

			#function to put everything in lower case
			def keepAlpha(sentence):
				alpha_sent = ""
				for word in sentence.split():
					alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
					alpha_sent += alpha_word
					alpha_sent += " "
				alpha_sent = alpha_sent.strip()
				return alpha_sent

			#function to stem feedback
			stemmer_fr = SnowballStemmer("french")
			def stemming_fr(sentence):
				stemSentence = ""
				for word in sentence.split():
					stem = stemmer_fr.stem(word)
					stemSentence += stem
					stemSentence += " "
				stemSentence = stemSentence.strip()
				return stemSentence

			#apply pre-processing to feedback
			sen_fr = sen_fr.lower()
			sen_fr = cleanPunc(sen_fr)
			sen_fr = keepAlpha(sen_fr)


			sen_fr  = stemming_fr(sen_fr)

			#make feedback a list - needed for further processing
			sen_fr = [sen_fr]

			#import vectorizer from trained data
			vectorizer_fr = deserialize('data/vectorizer_fr.pickle')

			#use the vectorizer for the right model
			vectorizer_fr = vectorizer_fr[section]

			#import alogrithms
			from sklearn.naive_bayes import MultinomialNB
			from sklearn.pipeline import Pipeline
			from sklearn.multiclass import OneVsRestClassifier


			#vectorize feedback
			pred_x_fr = vectorizer_fr.transform(sen_fr)

			#import possible tags file
			categories_fr = deserialize('data/categories_fr.pickle')

			#get possible tags from the right model
			categories_fr = categories_fr[section]

			#get predictions as a dictionary
			predictions_fr = {}
			for category in categories_fr:
				proba_fr = model_fr[section][category].predict_proba(pred_x_fr)
				predictions_fr[category] = proba_fr[-1][-1]

			#turn predictions into a dataframe
			preds_fr = pd.DataFrame(predictions_fr.items())

			#sort dataframe (highest probability at the top)
			preds_fr = preds_fr.sort_values(by=[1], ascending=False)

			#reset index
			preds_fr = preds_fr.reset_index(drop=True)

			#create list of proposed tags
			tags = []

			#get first tag
			tags.append(preds_fr[0][0])

			#get any other tag that's over 0.05 probablity - may need to tweak this figure
			rest = preds_fr[1:]
			other_tags = rest.loc[rest[1] >= .05]
			for tag in other_tags[0]:
				tags.append(tag)

			#convert tags to a string, split by a comma
			tag_str = ', '.join(tags)

	#process to follow if English
	else:
		#function to import pickle file
		def deserialize(file):
			with open(file, 'rb') as f:
				return pickle.load(f)

		#import English training model
		model_en = deserialize('data/model_en.pickle')

		#return empty strig if model doesn't exist
		if section not in model_en:
			tag_str = ''

		#if model exists, proceed
		else:

			#get feedback to process
			sen_en = request.args.get('text')

			#pre-process feedback the same way as the trained feedback
			if not sys.warnoptions:
				warnings.simplefilter("ignore")

			#function to clean the word of any punctuation or special characters
			def cleanPunc(sentence):
				cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
				cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
				cleaned = cleaned.strip()
				cleaned = cleaned.replace("\n"," ")
				return cleaned

			#function to put everything in lower case
			def keepAlpha(sentence):
				alpha_sent = ""
				for word in sentence.split():
					alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
					alpha_sent += alpha_word
					alpha_sent += " "
				alpha_sent = alpha_sent.strip()
				return alpha_sent

			#function to stem feedback
			stemmer_en = SnowballStemmer("english")
			def stemming_en(sentence):
				stemSentence = ""
				for word in sentence.split():
					stem = stemmer_en.stem(word)
					stemSentence += stem
					stemSentence += " "
				stemSentence = stemSentence.strip()
				return stemSentence

			#apply pre-processing to feedback
			sen_en = sen_en.lower()
			sen_en = cleanPunc(sen_en)
			sen_en = keepAlpha(sen_en)
			sen_en  = stemming_en(sen_en)


			#make feedback a list - needed for further processing
			sen_en = [sen_en]

			#import vectorizer from trained data
			vectorizer_en = deserialize('data/vectorizer_en.pickle')

			#use the vectorizer for the right model
			vectorizer_en = vectorizer_en[section]

			#import alogrithms
			from sklearn.naive_bayes import MultinomialNB
			from sklearn.pipeline import Pipeline
			from sklearn.multiclass import OneVsRestClassifier

			#vectorize feedback
			pred_x_en = vectorizer_en.transform(sen_en)

			#import possible tags file
			categories_en = deserialize('data/categories_en.pickle')

			#get possible tags from the right model
			categories_en = categories_en[section]

			#get predictions as a dictionary
			predictions_en = {}
			for category in categories_en:
				proba_en = model_en[section][category].predict_proba(pred_x_en)
				predictions_en[category] = proba_en[-1][-1]

			#turn predictions into a dataframe
			preds_en = pd.DataFrame(predictions_en.items())

			#sort dataframe (highest probability at the top)
			preds_en = preds_en.sort_values(by=[1], ascending=False)

			#reset index
			preds_en = preds_en.reset_index(drop=True)

			#create list of proposed tags
			tags = []

			#get first tag
			tags.append(preds_en[0][0])

			#get any other tag that's over 0.05 probablity - may need to tweak this figure
			rest = preds_en[1:]
			other_tags = rest.loc[rest[1] >= .05]
			for tag in other_tags[0]:
				tags.append(tag)

			#convert tags to a string, split by a comma
			tag_str = ', '.join(tags)

	return(tag_str)

if __name__ == '__main__':
    app.run()


#To see the autotag, you need to go to the local server, and add the attributes "lang", "section", and "text". E.g.: http://localhost:5000/suggestCategory?lang=en&section=Health&text=Where%20can%20I%20get%20masks?
