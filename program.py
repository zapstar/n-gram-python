import operator

fr = open('file.txt','r')

#define a sentence list
word_list = list()

#read all the lines in the file
lines = fr.readlines()
       
#FILE CLEANUP START	   
#Forget this part if you're data is clean (I mean usable)
#Change this appropriately to your requirements
#Please note that this has been customised to work on my
#data set.
for i in range(len(lines)):
    #strip the line of full stops and new lines in corners
    lines[i] = lines[i].strip()
    lines[i] = lines[i].strip('.')
    
    #if the line is not blank then
    if lines[i] != '':
        #if a to dialog is found, remove it
        if lines[i][0] == '[':
            j = lines[i].find(']')
            lines[i] = lines[i][j+2:]
        #split the line
        lines[i] = lines[i].split(" ")
        
        #Check if the word is not a part of act/scene definition
        if not lines[i][0].isupper() and lines[i][0] != 'Enter':
            #if not then add to the list
            for word in lines[i]:
                word_list.append(word)
				
#FILE CLEANUP END
#By now you should have a list of the words in the file
#There should not be unnecessary punctuation marks in the end
#of the words or any unnecessary whitespaces as well.
        
#now word_list contains a list, generate a n-gram
#print word_list

#n for n-gram
#Change it to whatever the requirement is
n = 6

ngrams = dict()

#create an n-gram list
for i in range(len(word_list) - n + 1):
    
    gram = tuple(word_list[i:i+n])
    
    if gram in ngrams:
        ngrams[gram] += 1
    else:
        ngrams[gram] = 1

#now ngrams contains all the ngrams of the book
sorted_ngrams = sorted(ngrams.iteritems(), key = operator.itemgetter(1), reverse = True)

#print the sorted n-grams
print sorted_ngramss