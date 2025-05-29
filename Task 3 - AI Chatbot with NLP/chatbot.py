import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load the intents file
with open('intents.json') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

# Loop through each intent in our intents.json file
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word in the pattern
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        # Add to documents list
        documents.append((word_list, intent['tag']))
        # Add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and lower each word and remove duplicates
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_words]
words = sorted(list(set(words)))

# Sort classes
classes = sorted(list(set(classes)))

# Print relevant information to see what we have
print(f"Words (unique lemmatized words): {words}")
print(f"Classes (intents): {classes}")
print(f"Documents (pattern, tag pairs): {documents}")

# Create the training data (bag of words)
training = []
output_empty = [0] * len(classes)

# Create bag of words for each document
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append(bag + output_row)

random.shuffle(training)
training = np.array(training)

# Split features and labels
train_x = list(training[:, :len(words)])
train_y = list(training[:, len(words):])

print("\nTraining data creation complete. Building prediction functions...")

# --- New Functions for Chatbot Logic ---

def clean_up_sentence(sentence):
    # Tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # Lemmatize each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words, show_details=False):
    # Tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # Bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # Assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print(f"found in bag: {s}")
    return np.array(bag)

def predict_class(sentence, words, classes, documents):
    # Predict the intent based on a simple matching logic
    # For a real chatbot, this would typically be a neural network's prediction.
    # Here, we'll find the document (pattern) that has the most matching words.

    p = bag_of_words(sentence, words, show_details=False)
    
    results = []
    for i, doc_bag in enumerate(train_x): # train_x holds bag of words for each document
        similarity = np.dot(p, doc_bag) # Simple dot product for similarity
        if similarity > 0: # If there's any overlap in words
            tag_index = np.argmax(train_y[i]) # Get the index of the intent tag
            intent_tag = classes[tag_index]
            results.append({'intent': intent_tag, 'score': similarity})
    
    # Sort results by score in descending order
    results.sort(key=lambda x: x['score'], reverse=True)
    
    if results:
        # We can add a threshold if needed, but for simplicity, take the best match
        return [{"intent": results[0]['intent'], "probability": results[0]['score']}] # probability is actually similarity score here
    else:
        return [] # No match found

def get_response(ints, intents_json):
    tag = ints[0]['intent'] if ints else "no_match" # Default to 'no_match' if no intent is found
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            # If a match is found, select a random response from that intent
            result = random.choice(i['responses'])
            break
    else: # If loop completes without finding a tag (i.e., tag was 'no_match')
        result = "Sorry, I don't understand that. Can you please rephrase?" # Default response for no match
    return result

# --- Main Chat Loop ---
print("\nBot is ready. Type 'quit' to exit.")
while True:
    message = input("You: ")
    if message.lower() == "quit":
        break
    
    ints = predict_class(message, words, classes, documents)
    if ints:
        res = get_response(ints, intents)
        print("Bot:", res)
    else:
        # If predict_class returns an empty list
        print("Bot: Sorry, I don't understand that. Can you please rephrase?")