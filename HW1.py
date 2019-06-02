from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords
import re

def get_error_type(pred, label):
    # return the type of error: tp,fp,tn,fn
    if pred == 1 and label == 1:
        return 'tp'
    elif pred == 1 and label == 0:
        return 'fp'
    elif pred == 0 and label == 1:
        return 'fn'
    elif pred == 0 and label == 0:
        return 'tn'

privative_list=["don't", "can't", "won't","isn't", "doesn't","couldn't","hasn't","didn't","weren't","aren't","wasn't", "wouldn't","haven't","Shouldn't","no","not","never","none",
                "nobody","nothing","nowhere","neither","hardly","scarcely","barely","little","few","seldom"]

degree_adverb = ["absolutely", "altogether", "completely", "entirely", "extremely", "fully", "perfectly", "quite", "thoroughly", "totally", "utterly", "wholly","badly", "bitterly",
                 "deeply", "enormously", "far", "greatly", "largely", "particularly", "profoundly", "so", "strongly", "terribly", "tremendously", "vastly", ]


def classify(text, inqtabs_dict, swn_dict):
    #return 1 if positive and 0 if negative
    regex = r'[A-Za-z]+\'?[A-Za-z]+'  # You'll probably want to update this regular expression
    words = re.findall(regex, text)

    Positive_score = 0
    Negative_score = 0
    i = 0  # type: int

    for word in words:
        word = word.lower()
        word = lemmatizer.lemmatize(word)

        if word in inqtabs_dict.keys():
            label = inqtabs_dict[word]

            if label == '1':
                Positive_score += 1
                for j in words[i-2 : i+2]:
                    if j in degree_adverb:
                        Positive_score += 1

                for w in words[i-3 : i+3]:
                    if w in privative_list:
                        Positive_score -= 1
                        Negative_score += 1

                        if w in degree_adverb:
                            Positive_score -= 1
                            Negative_score += 1



            elif label == '0':
                Negative_score += 1
                for j in words[i-2 : i+2]:
                    if j in degree_adverb:
                        Negative_score += 1

                for w in words[i-3 : i+3]:
                    if w in privative_list:
                        Positive_score += 1
                        Negative_score -= 1

                        if w in degree_adverb:
                            Positive_score += 1
                            Negative_score -= 1



        if word in swn_dict.keys():
            Positive_score += swn_dict[word][0]
            Negative_score += swn_dict[word][1]

            for j in words[i - 2: i + 2]:
                if j in degree_adverb:
                    Positive_score += swn_dict[word][0]
                    Negative_score += swn_dict[word][1]

            for w in words[i - 3: i + 3]:
                if w in privative_list:
                    Positive_score -= swn_dict[word][0]
                    Positive_score += swn_dict[word][1]
                    Negative_score -= swn_dict[word][1]
                    Negative_score += swn_dict[word][0]

                    if w in degree_adverb:
                        Positive_score -= swn_dict[word][0]
                        Positive_score += swn_dict[word][1]
                        Negative_score -= swn_dict[word][1]
                        Negative_score += swn_dict[word][0]



        i += 1


    return 1 if Positive_score > Negative_score+6.4 else 0




