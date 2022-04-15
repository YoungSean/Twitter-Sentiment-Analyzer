# Reference: https://www.youtube.com/watch?v=uPKnSq6TaAk&ab_channel=AISpectrum
# use Transformers package: https://github.com/huggingface/transformers/

from transformers import AutoTokenizer, AutoModelForTokenClassification
from scipy.special import softmax

tweet = "@lu_yangxiao  I am happy https://github.com/huggingface/transformers/"

## preprocess texts
tweet_entries = []

for word in tweet.split():
    if word.startswith('@') and len(word) > 1:
        word = '@user'
    elif word.startswith('http'):
        word = "http"
    tweet_entries.append(word)

print(tweet_entries)

tweet_processed = " ".join(tweet_entries)
print(tweet_processed)

roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForTokenClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ["Negative", "Neutral", "Positive"]

encode_tweet = tokenizer(tweet_processed, return_tensors='pt')
print(f"encoded tweet: {encode_tweet}")

output = model(**encode_tweet)
print(f"Output: {output}")

scores = output[0][0].detach().numpy()

scores = softmax(scores)

print(scores)