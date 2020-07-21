import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=15)
        fig.subplots_adjust(top=1.4)

    plt.imshow(wordcloud)
    plt.show()


def plot_nyt_word_incidence(df:pd.DataFrame, lookup_word:str, freq='M'):

    df['mention_tmp'] = df.abstract.str.extract(f'(\w*{lookup_word}\w*)')[0].notna()
    mask = df['mention_tmp']
    tmp = df.groupby([pd.Grouper(key='pub_date', freq=freq)]).mention_tmp.mean().sort_index()
    _ = tmp.plot(kind='bar', stacked=True, colormap='viridis',
                figsize=(12,6),
                title=f'Mentions About {lookup_word.title()} Over Time')\
        .set(xlabel='date', ylabel='article percentage')