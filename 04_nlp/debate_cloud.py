import pandas as pd
import numpy as np
from stop_words import get_stop_words

import matplotlib.pyplot as plt
import matplotlib as mpl

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

stop_words = get_stop_words('en')

STOPWORDS = ['re','ve','people','said','president','thing','united states','way'] + stop_words

df_pre = pd.read_csv('data/debate.csv', encoding="cp1252")

df = df_pre[['speaker','speech']]

text = df[df['speaker']=='Joe Biden']['speech'].tolist()
#print(text.head())

text = ' '.join(text).lower()

#print(text)

wordcloud = WordCloud(stopwords = STOPWORDS,
                        collocations=True).generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#print(df_pre.columns)
#print(df.head())
print(df['speaker'].value_counts())
