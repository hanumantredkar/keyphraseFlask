from functions import *

####################################################################################
############################# RUN FROM HERE ########################################
####################################################################################

inputTextDict = {1: 'The product is the best version of itself. I liked its make. I liked its features. I liked its appearence. Overall it is fantabulous.', 2: 'This is going to be the worst product. I like it but it is not as per my expectation. I am not recommending this product. Thankks'}

inputLocationDict = {1: 'Mapusa', 2: 'Panjim'}
  
dictFinalKeyphrasesLocation = runKeyphraseEngine(inputTextDict, inputLocationDict)


print('\nKEYPHRASE : LOCATION')
for keyphrase, location in dictFinalKeyphrasesLocation.items():
  print(keyphrase, '\t', location)