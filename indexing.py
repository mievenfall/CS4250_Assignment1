#-------------------------------------------------------------------------
# AUTHOR: Evelyn Vu
# FILENAME: indexing.py
# SPECIFICATION:  the Python program (search_engine.py) that will read the file collection.csv and
#                 output the precision/recall of a proposed search engine given the query q ={cat and dogs}. Consider
#                 the search engine will return all documents with scores >= 0.1.
# FOR: CS 4250- Assignment #1
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv
import math

documents = []
#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])

#Conducting stopword removal. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}

#Convert documents array into split word array for each doc
documents = [doc.split(" ") for doc in documents]

#Remove stopwords
for i, doc in enumerate(documents):
  new_doc = []
  for word in doc:
    if word not in stopWords:
      new_doc.append(word)
  documents[i] = new_doc

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love"
}

#Start stemming words
for doc in documents:
  for i, word in enumerate(doc):
    #Replaces with stem word if it exists or just itself if not
    doc[i] = steeming.get(word, word)

#Identifying the index terms.
#--> add your Python code here
terms = []

#Get terms
found_terms = set()

#Go through words in docs, if we have not encountered the current word, add it to terms
for doc in documents:
  for word in doc:
    if word not in found_terms:
      terms.append(word)
      found_terms.add(word)

#Helper functions for getting tf, df, idf, and tf-idf

def tf(word: str, doc: list[str]):
  return doc.count(word) / len(doc)

def df(word: str):
  count = 0
  for doc in documents:
    count += 1 if word in doc else 0
  return count 

def idf (word: str):
  return math.log(len(documents) / df(word), 10)

def tf_idf(word:str, doc: list[str]):
  return tf(word, doc) * idf(word)

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here
docTermMatrix = []

#Calculate matrix, term columns are love, cat, dog in this respective order
for i, doc in enumerate(documents):
  current_doc = []
  for term in terms:
    current_doc.append(round(tf_idf(term, doc), 4))
  docTermMatrix.append(current_doc)

#Printing the document-term matrix.
#--> add your Python code here
term_columns = "        "
for term in terms:
  if len(str(term)) < 4:
    term_columns +=  "|" + term + "    "
  else: 
    term_columns +=  "|" + term + "   "
print(term_columns)
for i, docTermWeights in enumerate(docTermMatrix):
  scores = "Doc " + str(i+ 1) + ":"
  for termWeight in docTermWeights:
    if len(str(termWeight)) < 4:
      scores += "\t|" + str(termWeight)
    else:
      scores += "\t|" + str(termWeight)
  print(scores)
print()