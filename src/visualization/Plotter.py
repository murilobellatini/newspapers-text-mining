import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

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


def plot_confusion_matrix(model, df:pd.DataFrame, features:np.array, labels:pd.Series, category_to_id:dict):
    """
    Trains and plots confusion matrix of model fitted to df with features and labels. 
    Returns fitted model, corresponding confusion matrix, y_test and y_pred.
    """
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    conf_mat = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(10,8))

    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=category_to_id.keys(), yticklabels=category_to_id.keys())

    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title(f'Confusion Matrix - {model.__class__.__name__} Text Classifier')

    plt.show()

    return model, conf_mat, y_test, y_pred, indices_test
