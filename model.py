from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re

class Model:

    preds_dict = {0:"Negative",1:"Positive"}
    tokenizer = None

    def __init__(self):

		#Loading the model
        self.model  = keras.models.load_model("LSTM")

		#Loading the tokenizer
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)


    def predict(self,test_text):

		#processing_text
        test_text  = [self.process_text(text) for text in test_text]

		#Tokenizing the text
        test_text  = self.tokenizer.texts_to_sequences(test_text)
		
        #Padding the text
        test_text  = pad_sequences(test_text,maxlen=49)

        pred       = self.model.predict_classes(test_text)[0][0] 

        return(self.preds_dict[pred])


    def emoji(self,text):

        # Smile -- :), : ), :-), (:, ( :, (-:, :') , :O
        text = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\)|:O)', ' positiveemoji ', text)
        # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
        text = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' positiveemoji ', text)
        # Love -- <3, :*
        text = re.sub(r'(<3|:\*)', ' positiveemoji ', text)
        # Wink -- ;-), ;), ;-D, ;D, (;,  (-; , @-)
        text = re.sub(r'(;-?\)|;-?D|\(-?;|@-\))', ' positiveemoji ', text)
        # Sad -- :-(, : (, :(, ):, )-:, :-/ , :-|
        text = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:|:-/|:-\|)', ' negetiveemoji ', text)
        # Cry -- :,(, :'(, :"(
        text = re.sub(r'(:,\(|:\'\(|:"\()', ' negetiveemoji ', text)

        return text            
                    
    def process_text(self,text):
        text = text.lower()                                             # Lowercases the string
        text = re.sub('@[^\s]+', '', text)                              # Removes usernames
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)   # Remove URLs
        text = re.sub(r"\d+", " ", str(text))                           # Removes all digits
        text = re.sub('&quot;'," ", text)                               # Remove (&quot;) 
        text = self.emoji(text)                                         # Replaces Emojis
        text = re.sub(r"\b[a-zA-Z]\b", "", str(text))                   # Removes all single characters
        text = re.sub(r"[^\w\s]", " ", str(text))                       # Removes all punctuations
        text = re.sub(r'(.)\1+', r'\1\1', text)                         # Convert more than 2 letter repetitions to 2 letter
        text = re.sub(r"\s+", " ", str(text))                           # Replaces double spaces with single space    

        return text
