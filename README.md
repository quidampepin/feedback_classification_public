# Autotagging web feedback by training a classification algorithm - Supervised training

These scripts were developed to help auto-tag web feedback gathered on Canada.ca pages.

There are 2 scripts:
- **process_feedback.py:** gets the data from AirTable, pre-processes the data, trains classification algorithms based on already tagged feedback (where tags have been confirmed by a human), and saves the necessary files in the data folder. Allows for training several models, depending on the topic of the page the feedback was gathered from.
- **suggest.py:** gets the feedback text to classify, gets the right files (the right model to use and its associated vectorizer and list of possible tags)

## How it works
The training and prediction happens in several phases.

### Data importing, splitting and pre-processing
- Data gets imported from a source (AirTable, CSV file, etc.), and is split between English and French
- Only samples that have a model assigned to them and confirmed tags are kept
- Sample are separated in different models
- Text is preprocessed to improve accuracy:
  - special characters are removed
  - text is changed to all lower case
  - text is stemmed, so only the roots are kept (e.g.: swim and swimming are considered the same words)

### Preparing the data for a classification algorithm
- Classification algorithms work with numbers, not words, so some preparation is needed
- Possible tags are turned into a sparse matrix: each tag is possible class, and each sample gets a 1 for tags that are assigned to it (and 0 for tags not assigned to it)
- Feedback text is changed into a matrix, where all words in the corpus are a possible attribute. Using a Term Frequency - Inverse document frequency (TF-IDF) vectorizer, each sample is turned into a vector, with a number assigned to the words (attributes) contained in the sample

### Train the algorithms
- Now that the sample text and the possible classes are numbers, a classification algorithm can be retrained
- Several options are possible, but this script uses a simple multinomial Naive Bayes classification algorithm
- For each model, a separate algorithm is trained for each possible tag, calculating the probability for each class
- The model, the vectorizer data and the possible tags for each model is saved in a pickle file.

### Get probabilities for each tag
- The prediction script launches a local web app
- The script looks for several attributes (language, model and text to classify), that are passed in the local URL
- The proper model, vectorizer and list of possible tags are downloaded, and a probability is calculated for each possible tag
- The script returns the tag with the highest probability, plus any other tag over a certain threshold
- The script in this repo works locally (localhost), but can be used to generate predictions on a live server


## Progressive improvement: re-training algorithm periodically

The Canada.ca feedback implementation records new feedback into an AirTable, and tags it automatically (if there's an existing model assigned to it).

Subject matter experts go over the new feedback, adjust the tag(s) if it's needed, and confirms the tag when they feel confident.

Every day, the prediction algorithm gets retrained with all confirmed tags. In effect, the prediction algorithm should get better with time, as more confirmed tags are used for training the algorithm.
