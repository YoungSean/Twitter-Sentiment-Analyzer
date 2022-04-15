# Reference: https://www.youtube.com/watch?v=uPKnSq6TaAk&ab_channel=AISpectrum
# use Transformers package: https://github.com/huggingface/transformers/

from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoConfig, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np

tweet = "@lu_yangxiao  I am happy https://github.com/huggingface/transformers/"

## preprocess texts

def preprocess(tweet):
    tweet_entries = []
    for word in tweet.split():
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_entries.append(word)

    return " ".join(tweet_entries)

tweet_processed = preprocess(tweet)
print(tweet_processed)

## Reference: https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
text = "Covid cases are increasing fast!"

def get_scores(text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    print(f"Scores: {scores}")
    return scores

scores = get_scores(text)

ranking = np.argsort(scores)
ranking = ranking[::-1]
for i in range(scores.shape[0]):
    l = config.id2label[ranking[i]]
    s = scores[ranking[i]]
    print(f"{i+1}) {l} {np.round(float(s), 4)}")
