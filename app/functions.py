import string
import numpy as np
import math
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.stem import WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

from collections import OrderedDict
from operator import itemgetter  # for getting top N largest items in a dictionary

  
def filterText(text):
  printableText = set(string.printable)
  if text in printableText:
    text = filter(text, printableText)
  else:
    text = text
  return text

def cleanText(text):
  text = text.lower()
  text = filterText(text)
  return text

def getLemmatizedText(postaggedtext):
  wordnet_lemmatizer = WordNetLemmatizer()
  lemmatizedText = []
  adjectiveTags = ['JJ', 'JJS', 'JJR']
  for word in postaggedtext:
    if word[1] in adjectiveTags:
      lemmatizedText.append(str(wordnet_lemmatizer.lemmatize(word[0], pos = "a")))
    else:
      lemmatizedText.append(str(wordnet_lemmatizer.lemmatize(word[0], pos = "n")))
  return lemmatizedText

def getAllStopwords(postaggedtext):
  #POS BASED FILTERING : POS based filtering by removing stopwords; here stopwords are words which are not nouns, adjectives, gerunds; Stopwords also contain punctuations
  stopwords = []
  wordTagsNotStopwords = ['NN', 'NNP', 'NNS', 'NNPS', 'JJ', 'JJR', 'JJS', 'FW', 'VBG']
  for word in postaggedtext:
    if word[1] not in wordTagsNotStopwords:
      stopwords.append(str(word[0]))
  punctuations = list(str(string.punctuation))
  stopwords = stopwords + punctuations
  stopwordlist = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
  #ADDITIONAL STOPWORDS : additional stopwords
  moreStopWords = []
  allStopWords = []
  moreStopWords = stopwordlist
  allStopWords = stopwords + moreStopWords
  allStopWords = set(allStopWords)
  return allStopWords

## This is a main KEYWORD EXTRACTION function ##
def extractKeywords(inputText):
  cleanedText = cleanText(inputText)
  tokenizedText = word_tokenize(cleanedText)
  postaggedtext = nltk.pos_tag(tokenizedText)    
  lemmatizedText = getLemmatizedText(postaggedtext)
  lemmatizedPosTaggedText = nltk.pos_tag(lemmatizedText)
  allStopWords = getAllStopwords(postaggedtext)
  #REMOVING STOPWORDS - Removing stopwords
  processedText = []
  for word in lemmatizedText:
    if word not in allStopWords:
      processedText.append(word)

  # UNIQUE TEXT : unique text from processed Text
  vocabulary = []
  vocabulary = set(processedText)
  vocabulary = list(vocabulary)  # Unique Processed Text
  
  #BUILDING TREEE RANK GRAPH : Building a Text Rank Graph for keyword extraction using TextRank Graph based model
  processedTextLength = len(processedText)
  vocabularyLength = len(vocabulary)
  weightedEdge = np.zeros((vocabularyLength, vocabularyLength), dtype = np.float32)
  score = np.zeros((vocabularyLength), dtype = np.float32)
  windowSize = 3
  coocurrences = []
  for i in range(0, vocabularyLength):
    score[i] = 1
    for j in range(0, vocabularyLength):
      if i == j:
        weightedEdge[i][j] = 0
      else:
        for startWindow in range(0, (processedTextLength - windowSize + 1)):
          endWindow = startWindow + windowSize
          window = processedText[startWindow:endWindow]
          if (vocabulary[i] in window) and (vocabulary[j] in window):
            iIndex = startWindow + window.index(vocabulary[i])
            jIndex = startWindow + window.index(vocabulary[j])
            if (iIndex, jIndex) not in coocurrences:
              weightedEdge[i][j] += 1/math.fabs(iIndex - jIndex)
              coocurrences.append([iIndex, jIndex])

  # UNDIRECTED EDGES : calculating weighted summation of word vertices
  undirectedEdge = np.zeros((vocabularyLength), dtype = np.float32)
  for i in range(0, vocabularyLength):
    for j in range(0, vocabularyLength):
      undirectedEdge[i] +=weightedEdge[i][j]
  
  # SCORING VERTICES 
  # score[i] = (1-d) + d x [ Summation(j) ( (weighted_edge[i][j]/inout[j]) x score[j] ) ] where j belongs to the list of vertices that has a connection with i. AND d is the damping factor.
  maxIterations = 50
  d = 0.85 #dumping factor
  t = 0.0001 # convergence threshold

  for iteration in range(0, maxIterations):
    previousScore = np.copy(score)
    for i in range(0, vocabularyLength):
      summation = 0
      for j in range(0, vocabularyLength):
        if weightedEdge[i][j] != 0:
          summation += (weightedEdge[i][j] / undirectedEdge[j]) * score[j]
      score[i] = (1 - d) + d * (summation)
    if np.sum(np.fabs(previousScore - score)) <= t:
      # print('Converging at iteration '+str(iteration)+'...')
      break

  # PHRASE PARTITIONIG : partitioning lemmatized words with dilimter as stopwords as phrases are also candidated for keywords/keyphrases
  phrases = []
  phrase = " "
  for word in lemmatizedText:
    if word in allStopWords:
      if phrase != " ":
        phrases.append(str(phrase).strip().split())
      phrase = " "
    elif word not in allStopWords:
      phrase += str(word)
      phrase += " "

  # UNIQUE PHRASES  : Creating list of unique phrases (candidate phrases)
  uniquePhrases = []
  for phrase in phrases:
    if phrase not in uniquePhrases:
      uniquePhrases.append(phrase)

  # THINNING CANDIDATE KEYPHRASES : thinning the list of candidate keyphrases i.e., removing single word keywords from the candidate keyphrases
  for word in vocabulary:
    for phrase in uniquePhrases:
      if (word in phrase) and ([word] in uniquePhrases) and (len(phrase) > 1):
        uniquePhrases.remove([word])

  # SCORING KEYPHRASES
  phraseScores = []
  keyphrases = []
  for phrase in uniquePhrases:
    phraseScore = 0
    keyphrase = ''
    for word in phrase:
      keyphrase += str(word)
      keyphrase += " "
      phraseScore += score[vocabulary.index(word)]
    phraseScores.append(phraseScore)
    keyphrases.append(keyphrase.strip())
  i = 0
  return vocabulary, score, keyphrases, phraseScores

def getDictionaryOfKeywordsAndKeyphrases(inputText):
  # print('This is a printscreen')
  keywords, wordScores, keyphrases, phraseScores = extractKeywords(inputText)
  # Creating Dictionary of (Keyword, wordScore) pair and (Keyphrase, phrasescore) pair
  dictKeywords = dict(zip(keywords, wordScores))
  dictKeyphrases = dict(zip(keyphrases, phraseScores))
  return dictKeywords, dictKeyphrases

def runKeyphraseEngine(inputTextDict, inputLocationDict):
  reviewString = {}
  dictKeywords = {}
  dictKeyphrases = {}
  dictKeywordsMerged = {}
  dictKeyphrasesMerged = {}
  dictKeyphraseLocation = {}
  dictKeyphraseLocationMerged = {}
  for reviewNo, reviewText in inputTextDict.items():
    reviewString[reviewNo] = {reviewNo:reviewText}
    dictKeywords[reviewNo], dictKeyphrases[reviewNo] = getDictionaryOfKeywordsAndKeyphrases(reviewText)

    if not dictKeywordsMerged:
      d = {}
      dict_a = dictKeywordsMerged
      dict_b = dictKeywords[reviewNo]
      for k, v in dict_a.items():
        if k in dict_b:
          val1 = (v + dict_b[k]) / 2 # average sum of ele1 and ele2 in each value list
          d[k] = val1 # set new value to key
          del dict_b[k] # remove key
        else:
          d[k] = v # else just add the k,v
      dictKeywordsMerged.update(dict_b) # update with remainder of dict_b
    else:
      dictKeywordsMerged.update(dictKeywords[reviewNo])

    if not dictKeyphrasesMerged:
      d = {}
      dict_a = dictKeyphrasesMerged
      dict_b = dictKeyphrases[reviewNo]
      for k, v in dict_a.items():
        if k in dict_b:
          val1 = (v + dict_b[k]) / 2 # average sum of ele1 and ele2 in each value list
          d[k] = val1 # set new value to key
          del dict_b[k] # remove key
        else:
          d[k] = v # else just add the k,v
      dictKeyphrasesMerged.update(dict_b) # update with remainder of dict_b
    else:
      dictKeyphrasesMerged.update(dictKeyphrases[reviewNo])

    for key, value in dictKeyphrases[reviewNo].items():
      dictKeyphraseLocation[key] = inputLocationDict[reviewNo]        
      dictKeyphraseLocationMerged.update(dictKeyphraseLocation.items())

  # print(dictKeyphraseLocationMerged)
  # print(dictKeyphrasesMerged)
  N = 25
  topKeyphrases = {}
  topKeyphrases = dict(sorted(dictKeyphrasesMerged.items(), key = itemgetter(1), reverse = True)[:N]) 

  # print('\n')
  # print('\nExtracted Keyphrase -> Confidence Score')
  # for keyphrase, confscore in topKeyphrases.items():
    # print(keyphrase, '\t', confscore)

  a = topKeyphrases
  b = dictKeyphraseLocationMerged
  c = {}
  for key, value in a.items():
    if key in b.keys():
      c.update({key:b[key]})
  topKeyphraseAndLocation = c

  # print('\nKEYPHRASE : LOCATION')
  # for keyphrase, location in topKeyphraseAndLocation.items():
    # print(keyphrase, '\t', location)

  verbList = ['VB', 'VBN', 'VBG']

  a = topKeyphraseAndLocation
  dictSelectedKeyLoc = dict('')
  tokString = []
  for key, value in a.items():
    tokenisedList = word_tokenize(key)
    postaggedList = nltk.pos_tag(tokenisedList)
    for item in postaggedList:
      for subitem in item:
        if subitem in verbList:
          dictSelectedKeyLoc.update({key:value})  
  b = dictSelectedKeyLoc
  set1 = set(a.items())
  set2 = set(b.items())
  dictFinal = dict(set1 ^ set2)
  # print('\nKEYPHRASE : LOCATION')
  # for keyphrase, location in dictFinal.items():
    # print(keyphrase, '\t', location)

  dictFinalKeyphrasesLocation = {}
  for key, value in topKeyphrases.items():
    for keyL, location in dictFinal.items():
      if key == keyL: 
      # dictFinalKeyphrasesLocation[key] = value
      # val = dictFinal.values()[key]
        dictFinalKeyphrasesLocation.update({key:location})
        break
      
  # print('\nKEYPHRASE : LOCATION')
  # for keyphrase, location in dictFinalKeyphrasesLocation.items():
    # print(keyphrase, '\t', location)
  return dictFinalKeyphrasesLocation
  # return nothing