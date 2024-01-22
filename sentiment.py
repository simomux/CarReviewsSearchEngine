from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax

# The model isn't really trained on car reviews, but it's surprisingly accurate
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

max_length = 512  # Max amount of tokens


def sentiment_analysis(results):
    for result in results:
        print(f"\nFile:{result['file']}")
        text = result["content"]

        # Trunking reviews that exceed 512 tokens
        encoded_input = tokenizer(text, max_length=max_length, return_tensors='pt', truncation=True)

        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        print(scores)

        # Ui for printing scores
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            label = config.id2label[ranking[i]]
            score = scores[ranking[i]]
            print(f"{i + 1}) {label} {np.round(float(score), 4)}")


def index_sentiment(string):
    # Trunking reviews that exceed 512 tokens
    encoded_input = tokenizer(string, max_length=max_length, return_tensors='pt', truncation=True)

    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores


if __name__ == "__main__":
    text = """I find this truck to be average. It 
has the steering thump noise, found in 
chevy trucks since 1999 that chevy 
won't solve. Also had mildew smell in 
the air conditioner, the dealer 
installed a circuit board to correct 
this. Also the truck has the common 
transmisson shudder on acceleration."""
    encoded_input = tokenizer(text, max_length=max_length, return_tensors='pt', truncation=True)

    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    print(scores)

    # Ui for printing scores
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    for i in range(scores.shape[0]):
        label = config.id2label[ranking[i]]
        score = scores[ranking[i]]
        print(f"{i + 1}) {label} {np.round(float(score), 4)}")