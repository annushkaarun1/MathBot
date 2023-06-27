# imports all the necessary libraries and modules needed
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
from googlesearch import search
import ssl
import json
import nltk
from nltk.stem import WordNetLemmatizer
import smtplib
import time

# certificate issue (on my end) this bit of code resolves by handling environment which doesn't support the HTTPS cert verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
#---------------------------------------------------------------------------


nltk.download('popular', quiet=True) #for downloading packages

# uncommented only to download for the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the contents for chatbot
with open('chatbotinfo.txt','r', encoding='utf8', errors ='ignore') as contents:
    rawInformationOnChatbot = contents.read().lower() #puts everything in lower case

with open('botIntents.json','r') as f: # opens intents file for chatbot to respond
    intentsData = json.load(f) #loads in json format

writetofile = open("ChatBotConversation.txt", "a")

#Tokenisation
sent_tokens = nltk.sent_tokenize(rawInformationOnChatbot)# converts to list of sentences
word_tokens = nltk.word_tokenize(rawInformationOnChatbot)# converts to list of words

lemmer = WordNetLemmatizer() # creates the function of lemmatizing under the name 'lemmer'

def LemmatizeTokens(tokens): # function to lemmatize the input
    return [lemmer.lemmatize(token) for token in tokens] # lemmatizes each token in sentence

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation) # removes any punctuation using dict

def LemNormalize(text): # function to the tokenize the input message
    return LemmatizeTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict))) # tokenizes the sentence


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey", "wassup", )
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
ignore_letters = ['?','!','.',','] #punctuation to ignore

def greeting(sentence): # function to return a greeting response
    for word in sentence.split(): # for loop for each word in the sentence (split up)
        if word.lower() in GREETING_INPUTS: # if the word is in the list greeting_inputs
            return random.choice(GREETING_RESPONSES) # a random choice from the list greeting responses is chosen and used

def inIntents(sentence): # function to determine whether input is in botIntents.json file
    for intent in intentsData['intents']: # for each intent in the intents file
        if sentence in intent['patterns']: # if the input sentence is in the patterns tag
            print(random.choice(intent['responses'])) # it prints a random choice from the responses

def search_query(query, index=0): # function to output first 3 urls from a google search of the input
    fallback = 'Sorry, I cannot think of a reply for that.' # creates a standard response if the search fails
    result = '' # empty string

    try: # exception handling
        search_result_list = list(search(query, tld="com.my", num=3, stop=3, pause=1)) # finds the search results and stores in a list
        # uses the top level domain '.com.my' since the google is in the Malaysian server
        # num = 3 indicates the number of urls to be found
        # stop = 3 indicates the last result to be retrieved
        # pause = 1 indicates the lapse to wait between HTTP requests

        for i in search_result_list: # for loop for each result in the search result list
            writetofile.write(i) # it is appended to the end of the file
            writetofile.write("\n") # a new line is added
        return(search_result_list) # the search result list is returned

    except: # if this does not work
        if len(search_result_list) == 0: # the length of the search result is 0
            result = fallback # result is set to the fall back standard message
        return result # the result is returned



# Generating response

def response(user_response): # function for generating the user response from the text file
    initial_response = '' # initially empty string
    sent_tokens.append(user_response) # appends the user's response to the sent_tokens string
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english') # transforms the text into a vector to anayse the frequency of the words in user response.
    # stop words is the only string value supported (english words)
    tfidf = TfidfVec.fit_transform(sent_tokens) # Transforms sent_tokens to a matrix (row = sentence, column = words, table values = count)
    vals = cosine_similarity(tfidf[-1], tfidf) # dot product of the previous value of the tfidf
    idx=vals.argsort()[0][-2] # sorts the values and returns the index serial and gets second largest element's index
    flat = vals.flatten() # inserts the 2d array from previous line into a 1d array
    flat.sort()
    req_tfidf = flat[-2] # flattens into an array
    if req_tfidf == 0: #if the weighting is 0
        initial_response = initial_response + "I am sorry! I don't understand you" # the string is appended to the existing variable
        return initial_response # returns initial_response
    else: # if it is not 0
        initial_response = initial_response + sent_tokens[idx] # the corresponding output is presented
        return initial_response # returns initial_response


#------ appends of all the patterns in the file botIntents.json to a list ------

allpatterns = [] #empty list

firstTag=(intentsData['intents'][0]) # parses the botIntents.json file for each intent
firstTagPatterns = firstTag['patterns'] # finds the patterns of each tag (greetings, goodbye, name and purpose)
for i in firstTagPatterns: # appends each element in the list to the empty list allpatterns
    allpatterns.append(i)

secondTag=(intentsData['intents'][1])
secondTagPatterns = secondTag['patterns']
for i in secondTagPatterns:
    allpatterns.append(i)

thirdTag=(intentsData['intents'][2])
thirdTagPatterns = thirdTag['patterns']
for i in thirdTagPatterns:
    allpatterns.append(i)

fourthTag=(intentsData['intents'][3])
fourthTagPatterns = fourthTag['patterns']
for i in fourthTagPatterns:
    allpatterns.append(i)

def final_Response(msg): # subroutine for all the possible user inputs
    tobewritten = "User: " + msg # stores the user's input along with the prefix 'user: '
    writetofile.write(tobewritten) # the text in the variable tobewritten is appended to the file ChatBotConversation.txt using the writetofile function
    writetofile.write("\n") # a new line is added
    user_response = msg.lower() # converts the user response to lowercase letters
    if user_response != 'bye': # if the user response is not bye (or an indication of conversation end)
        if user_response == 'thanks' or user_response == 'thank you': # if the user response is thanks or thank you (also an indication of end of conversation)
            writetofile.write("End of Conversation" + "\n") # the phrase 'end of conversation' is writter to the next line in the file and a new line is added
            return("You are welcome") # 'you are welcome; is printed on the screen and the conversation is over

        elif user_response.split()[0] == "search": # the user response is split and the first word of the input is compared to the string 'search'
            user_response = user_response.split(' ', 1)[1] # if the first part of the user's input is 'search', the rest of the input (aFter the word search) is taken
            return("Here are links to your search: ", search_query(user_response)) # the subroutine returns the output of the function 'search_query' with the input as the user's search request prefixed with 'Here are links to your search: '

        elif user_response not in allpatterns: # if the user's input is not in the list allpatterns (which contains all the possible user inputs which have been predifend by the file botIntents.json)
            print("MathBot: ", end="") #prints the
            writetofile.write("MathBot: " + response(user_response) + "\n") # the user input is appended to the file ChatBotConversation.txt with a new line
            sent_tokens.remove(user_response) # removes the user's response from the list sent_tokens
            time.sleep(1)
            return(response(user_response)) # calls the function 'response' using the user's input as the argument
            # this function also outputs the standard "I am sorry! I don't understand you" if the input is not understood by the bot
        else: # if the user's input is not any of the above
            for intent in intentsData['intents']: # parses the intents tags with a for loop
                for i in intent['patterns']: # looks at each value in the patterns tag
                    i.lower() # makes each word lowercase
                    if user_response == i: # if the input is the same as any of the words
                        writetofile.write("MathBot: " + random.choice(intent['responses'])+ "\n") # the user response is added to the text file "ChatBotConversation.txt" using the writetofile function along eith the corresponding random output from the 'responses' tag of the botIntents.json
                        time.sleep(1)
                        return(random.choice(intent['responses'])) # prints the randomised response from the response tag to the user