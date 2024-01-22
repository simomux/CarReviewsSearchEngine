# Old Bert model
# DEPRECATED

'''from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline


def sentiment_analysis(results):
    finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

    nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

    for result in results:
        file_name = result["file"]
        content = result["content"]

        # Tokenizza il testo e ottieni la lista di token
        tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(content, max_length=512, truncation=True)))

        # Se i token superano ancora il limite di 512, prendi solo i primi 512 token
        if len(tokens) > 512:
            tokens = tokens[:512]

        # Ricostruisci il testo dai token
        truncated_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(tokens))

        # Calcola il sentiment analysis sul testo tokenizzato
        sentiment_result = nlp(truncated_text)

        print(f"File: {file_name}")
        print(f"Sentiment: {sentiment_result}")'''

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax


def sentiment_analysis(results):
    # The model isn't really trained on car reviews, but it's surprisingly accurate
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    max_length = 512  # Max amount of tokens

    for result in results:
        print(f"\nFile:{result['file']}")
        text = result["content"]

        # Trunking reviews that exceed 512 tokens
        encoded_input = tokenizer(text, max_length=max_length, return_tensors='pt', truncation=True)

        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Ui for printing scores
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            label = config.id2label[ranking[i]]
            score = scores[ranking[i]]
            print(f"{i + 1}) {label} {np.round(float(score), 4)}")
