# Email Forensic Language Processing library
# The purpose of this library is to experiment with email forensics and NLP
# This library is developed in partial fulfillment to MIT 807 at the University of Pretoria

# Required for the email handling class
import email    # Standard python email parsing library
from gensim.summarization import summarize
from gensim.summarization import keywords
from gensim.parsing.preprocessing import strip_multiple_whitespaces

# Required imports for additional functions used in pipeline processing
import nltk
import re
import os
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

print("Importing Spacy")
import spacy
#import textacy

import json

print("Loading encore web")
spacy_nlp = spacy.load('en_core_web_lg')
#spacy_nlp = spacy.load('en_core_web_sm')
print('Importing contractions')
from pycontractions import Contractions
contractions = Contractions(api_key="glove-twitter-100")
print("Loading glove")
contractions.load_models()
print("Initialisation of eflp complete.")



##### Some definitions ######
FORMATTING_REGEX = r"=\n|=\d+"

EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""


HTML_REGEX = r"<.*?>"
CHARACTERS_REGEX = r"[,_]"
BELONG_REGEX = r"'s"
ENRON_EMAIL_REGEX = r"/\w+/\w+/\w+@\w+|/\w+/\w+@\w+|/\w+@\w+|/\w+/Enron Communications@Enron Communication|/HOU/\w+|/NA/\w+|@ENRON"
TWO_LETTERS_REGEX = r"\b[\w]{1,2}\b"

# Standard
FORMATTING = re.compile(FORMATTING_REGEX,flags=re.IGNORECASE)
URL= re.compile(URL_REGEX,flags = re.IGNORECASE)
EMAIL = re.compile(EMAIL_REGEX,flags = re.IGNORECASE)
HTML = re.compile(HTML_REGEX,flags = re.IGNORECASE)
CHARACTERS = re.compile(CHARACTERS_REGEX,flags = re.IGNORECASE)


#Additional
EMAIL_ENRON = re.compile(ENRON_EMAIL_REGEX,flags  = re.IGNORECASE)
TWO_LETTERS = re.compile(TWO_LETTERS_REGEX,flags = re.IGNORECASE)


NAME_REGEX = "[P,p]hillip|[A,a]llen"
NAME = re.compile(NAME_REGEX, flags = re.IGNORECASE)





##### Define the email handler class and associated functions #######
# We want to design a class to handle a single email.
class Email_Forensic_Processor:
    # Standard init function of the class
    def __init__(self):
        self.src_file = None              # Path to the original mail file
        self.obj_file = None              # This object if it is saved
        self.raw_mail = None              # Original raw email
        self.body = None                  # Extracted raw body
        self.subject = None               # Extracted raw subject
        self.pre_processed_body = None    # Basic pre-processed body
        self.summary = None               # Stored summary of the body
        self.keywords = None              # Stored keyword from the summary of the body
        self.originator= None             # The extracted "From"
        self.recipients = None            # The extracted "To", "cc" and "bcc"
        self.body_people = []             # Detected names in the body of the email
        self.body_orgs = []               # Detected organisations in the body of the mail
        self.body_forward = False         # Forwarded email content detected
        self.body_tokens = None           # The body as tokenized words 
        self.body_bow = None              # Bag of words representation of the body
        self.body_email_addr = None       # List of additional email addresses detected in the body
        self.body_urls = None             # List urls detected in the body of the email
        self.body_pos_string = ''         # Extract parts of speech as a long string
        self.body_pos_tokens = None       # The extracted tokens
        

    # Store the mail object.
    def initMail(self, filename, preProcess = True):
        self.__init__()
        self.src_file = filename
        with open (filename, "r") as inputFile:
            try:
                self.raw_mail = inputFile.read()
            except:
                print("-----------------------------")
                print("filename: ",filename," posed a problem during loading.")
                print("-----------------------------")

        parsed_mail = email.parser.Parser().parsestr(self.raw_mail)

        self.body = parsed_mail.get_payload()
        self.subject = parsed_mail.get('subject')
        self.originator = parsed_mail.get('from')
        self.recipients = parsed_mail.get('to')

        if preProcess:
            self.preProcess()
            
    def saveMail(self,filename):
        #if not (os.path.splitext(filename)[-1] == "json"):
            #filename = filename + ".json"
        self.obj_file = filename
        with open (filename, "w") as outputFile:
            json.dump(self.__dict__, outputFile, default = lambda o: o.__dict__)

    def loadMail(self,filename):
        filename = filename + ".json"
        with open (filename, "r") as inputFile:
            self.__dict__ = json.load(inputFile)


        
        
    # Call the Gensim summariser in standard form to generate and store a summary.
    def createSummary(self,input = "raw"):
        if input == "raw":
            try:
                self.summary = summarize(self.body,split=True)
                self.keywords = keywords(self.body)
            except:
                print('Cannot summarise this email.')
                pass
        elif input == "pre-processed":
            try:
                self.summary = summarize(self.pre_processed_body,split=True,word_count = 200)
                self.keywords = keywords(self.pre_processed_body)
            except:
                print('Cannot summarise this email.')
                pass

    # Perform pre-processing on the email body and store it.
    def preProcess(self, type="full"):
        self.pre_processed_body = self.body
        # Standard essential preprocessing that must take place 
        self.remove_justify()
        self.remove_forward()
        self.remove_patterns(pattern_list = [EMAIL,
                                             NAME,
                                             URL,
                                             HTML,
                                             CHARACTERS]) # Remove specific patterns, e.g. additioal \n, =09 etc.
        self.replaceContractions()
        self.remove_patterns(pattern_list = [TWO_LETTERS])  # Remove any remaining one and two letter words not expanded.
        
        if type == "full":  # If full preprocess is to take place
            self.remove_patterns(pattern_list = [EMAIL_ENRON])
            self.finalise_preprocess()
            
    def finalise_preprocess(self):
        # This is a helper function used when only a partial preprocess was run with manual steps added in the middel.
        self.tokenize()
        self.lemmatize()
        self.remove_stopwords()
        self.detectEntities()

    def remove_justify(self):
        new_text = ""
        lines = re.findall(r".+\n", self.pre_processed_body, flags=0)
        for line in lines:
            if len(line) == 79:
                line = re.sub(r"\n","",line)
            elif len(line) == 77:
                line = re.sub(r"=\n","",line)
            elif len(line) == 75:
                line = re.sub(r"\n","",line)

            new_text += line
        self.pre_processed_body = new_text

    def remove_forward(self):
        if re.search(r"(-+ Forwarded by .+Subject:)",self.pre_processed_body,flags=re.DOTALL) == None:
            #print(re.search(r"(-+ Forwarded by .+Subject:)",text))
            pass
        else:
            #print("Removing forward")
            self.pre_processed_body = re.sub(r"(-+ Forwarded by .+Subject:)","",self.pre_processed_body,flags=re.DOTALL)
            self.pre_processed_body = re.sub(r"^.+\n","",self.pre_processed_body)
        



    def remove_patterns(self,pattern_list = None):
        if pattern_list == None:
            #pattern_list = [FORMATTING,EMAIL,URL,EMAIL_ENRON,HTML,CHARACTERS,TWO_LETTERS]
            pass  # If no pattern list is passed, do nothing.
        for pattern in pattern_list:
            self.pre_processed_body = pattern.sub('',self.pre_processed_body)      

    def replaceContractions(self):
        generator = contractions.expand_texts([self.pre_processed_body])
        for text in generator:
            self.pre_processed_body = text

    def tokenize(self):
        # Split the text string into tokens.
        # ref - https://radimrehurek.com/gensim/auto_examples/tutorials/run_lda.html#sphx-glr-auto-examples-tutorials-run-lda-py

        # Turn all text to lower case, detect word and tokenize
        tokenizer = RegexpTokenizer(r'\w+')
        text = self.pre_processed_body.lower()
        tokens = tokenizer.tokenize(text)

        # Remove identified tokens
        removal_list = []
        for token in tokens:
            if token.isnumeric():
                removal_list.append(token)

        for marked_token in removal_list:
            tokens.remove(marked_token)
        self.body_tokens = tokens

    def lemmatize(self):
        lemmatizer = WordNetLemmatizer()
        lem_tokens = []
        for token in self.body_tokens:
            lem_tokens.append(lemmatizer.lemmatize(token))
        self.body_tokens = lem_tokens

    def remove_stopwords(self):
        stop_words = stopwords.words('english')
        #stop_words.extend(['from', 'subject', 're','forward','to','cc','am','pm',"forwarded"])
        filtered_tokens = []
        for word in self.body_tokens:
            if word not in stop_words:
                filtered_tokens.append(word)
        self.body_tokens = filtered_tokens

    def detectEntities(self):
        doc=spacy_nlp(self.pre_processed_body)
        for entity in doc.ents:
            if entity.label_ == 'PERSON':
                self.body_people.append(entity.text)
            if entity.label_ == 'ORG':
                self.body_orgs.append(entity.text)
        for token in doc:
            if token.pos_ == "VERB" or token.pos_ == "NOUN" or token.pos_ == "PROPN":
                self.body_pos_string = self.body_pos_string + ' ' + token.lemma_
                
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(self.body_pos_string.lower())

        # Remove identified tokens
        removal_list = []
        for token in tokens:
            if token.isnumeric():
                removal_list.append(token)

        for marked_token in removal_list:
            tokens.remove(marked_token)
        self.body_pos_tokens = tokens


            
                

# Alies for our class for backward compatibility with existing code
class Summary(Email_Forensic_Processor):
    pass

    

        
####  Define additional functions used in pipeline processing ##########
######### Funcitons that can be called directly. These functions serve as helper functions for the queue functions

def tokenize(text):
    # Split the text string into tokens.
    # ref - https://radimrehurek.com/gensim/auto_examples/tutorials/run_lda.html#sphx-glr-auto-examples-tutorials-run-lda-py
    
    # Turn all text to lower case, detect word and tokenize
    tokenizer = RegexpTokenizer(r'\w+')
    text = text.lower()
    tokens = tokenizer.tokenize(text)

    # Remove identified tokens
    removal_list = []
    for token in tokens:
        if token.isnumeric():
            removal_list.append(token)

    for marked_token in removal_list:
        tokens.remove(marked_token)
    return tokens

def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lem_tokens = []
    for token in tokens:
        lem_tokens.append(lemmatizer.lemmatize(token))
    return lem_tokens

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = []
    for word in tokens:
        if word not in stop_words:
            filtered_tokens.append(word)
    return filtered_tokens

def remove_patterns(string):
    EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    EMAIL_REGEX_2 = r"""/HOU/ECT@ECT"""
    EMAIL_REGEX_3 = r"""/HOU/ECT"""


    
    new_string = re.sub(EMAIL_REGEX,'',string)
    new_string = re.sub(EMAIL_REGEX_2,'',new_string)
    new_string = re.sub(EMAIL_REGEX_3,'',new_string)
    new_string = re.sub(URL_REGEX,'url_removed',new_string)
    return new_string

def detect_something(text):
    # url = "https://www.randomlists.com/email-addresses"
    EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    EMAIL_REGEX_2 = r"""/HOU/ECT@ECT"""
    EMAIL_REGEX_3 = r"""/HOU/ECT"""
    

    
    for re_match in re.finditer(EMAIL_REGEX, text):
        print(re_match.group())
        
    for re_match in re.finditer(URL_REGEX, text):
        print(re_match.group())

######### Wrapper functions to for queueing for text processing

# Dummy function to illustrate the required function template
def dummy(in_q,out_q,**kwargs):
    # Initialise whatever needs to be initialised here
    while in_q:  #loop readig the in_q
        text = in_q.get() #By default blocks
        # Perform operations on the text here
        out_q.put(text)

def pipe_tokenize(in_q,out_q,**kwargs):


    # Input: Must be a string
    # Output: A list of tokens, possibly empty

    # Initialise whatever needs to be initialised here
    stopwords_ = set(stopwords.words('english'))
    while in_q:  #loop readig the in_q
        text = in_q.get() #By default blocks
        tokens = []
        filtered_tokens = []
        if type(text) is str:
            if text != "":
                # Remove stop words by iterating through the words
                # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
                for sent in nltk.sent_tokenize(text):
                    for word in nltk.word_tokenize(sent):
                        tokens.append(word.lower())
                # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
                for token in tokens:
                    if re.search('[a-zA-Z]', token):
                        filtered_tokens.append(token)
        out_q.put(filtered_tokens)


def test(**kwargs):
    # Remove stopwords in English.  Modelled on example at http://brandonrose.org/clustering#Latent-Dirichlet-Allocation

    # Input: Must be a string
    # Output: A list of tokens, possibly empty

    if(kwargs['mode'] == 'textpipe'):
        # Initialise whatever needs to be initialised here
        in_q = kwargs['in_q']
        out_q = kwargs['out_q']
        while in_q:  #loop readig the in_q
            text = in_q.get() #By default blocks
            tokens = __tokenize__(text)
            out_q.put(filtered_tokens)
    elif(kwargs['mode'] == 'text'):
        text = kwargs['text']
        return __tokenize__(text)