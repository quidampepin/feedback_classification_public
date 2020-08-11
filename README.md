# Autotagging web feedback by training a classification algorithm - Supervised training

These scripts were developed to help auto-tag web feedback gathered on Canada.ca pages. There are 2 scripts:
- process_feedback.py: gets the data from AirTable, pre-processes the data, trains classification algorithms based on already tagged feedback (where tags have been confirmed by a human), and saves the necessary files in the data folder. Allows for training several models, depending on the topic of the page the feedback was gathered from.
- suggest.py: gets the feedback text to classify, gets the right files (the right model to use and its associated vectorizer and list of possible tags)

## How it works
- Content to come

## Progressive improvement: re-training algorithm periodically

- Content to come
