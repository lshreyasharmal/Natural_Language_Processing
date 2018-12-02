import nltk
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim

model = gensim.models.KeyedVectors.load_word2vec_format(r'C:\Users\MyPC\Desktop\NLP 6\GoogleNews-vectors-negative300.bin/GoogleNews-vectors-negative300.bin', binary=True)  
print(model.wv.most_similar(positive=['China', 'Delhi'], negative=['India'])[0])
print(model.wv.most_similar(positive=['USA', 'ISRO'], negative=['India'])[0])
