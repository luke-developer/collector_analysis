from __future__ import print_function
import nltk
import codecs
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# used to get the base/dictionary form of words, aka lemma
lemmatizer = WordNetLemmatizer()

# Import our text file, convert all to lower case
# to help with processing later on
file_01 = codecs.open("t0aa","r",('utf-8'))
file_read = file_01.read().lower()

# set our tokenizer so that it ignores punctuation
# will only get one or more word characters, no numbers either
custom_toke = RegexpTokenizer(r"[a-zA-Z]+")

# tokenizer, used to segment words
toker = custom_toke.tokenize(file_read)

## test file has been input
## test_import = [print(i) for i in toker]
## test passes, text print to console

# import our stopworder
stops = set(stopwords.words("english"))

## test stopwords are imported correctly
## test_stops = [print(i) for i in stops]
## test passes, list of stop words prints to terminal

# loop through document and output
# new document with stopwords removed
remove_stops = [i for i in toker if i not in stops]

# find the frequency of words in our new clean text
fdlist = FreqDist(remove_stops)
# assign the top one hundred most frequently occuring words
most_common = str(fdlist.most_common(100))

# output the result of the top 100 to a new text file
with open("output_file.txt","w") as output:
    output.write(most_common)
