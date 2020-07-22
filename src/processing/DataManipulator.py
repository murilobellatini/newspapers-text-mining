import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.feature_selection import chi2
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer


def breakdown_cat_distribution(df:pd.DataFrame, cat_columns:list):
    """
    Displays classes distribution of categorial classes in absolute and relative values.
    - df: DataFrame to be explroed
    - cat_columns: categorical columns
    """
    print(f'DatFrame columns breakdown\n' + 20 * '=')
    for col in cat_columns:
        print(f'\nColumn `{col}` distribution')
        tmp = pd.concat([
                df[col].value_counts(normalize=False, dropna=False).apply('{:,}'.format).rename('count'),
                df[col].value_counts(normalize=True, dropna=False).apply('{:.1%}'.format).rename('percentage')
            ], axis=1)
        display(tmp)

def get_most_correlated_tokens(features:np.array, labels:pd.Series, vectorizer:TfidfVectorizer, category_to_id:dict, top_n_tokens:int=3):
    """
    Returns DataFrame with most correlated tokens of each category present in `category_to_id`, methodology is Chi Squared.
    - features: numpy array of text features (result of vectorizer)
    - labels: pandas Seires with target labels factorized (numeric values)
    - vectorizer: vectorizer used for featurizing text
    - top_n_tokens: top most correlated tokens to be returned
    - category_to_id: dictionary to translate labels to human readable format
    """

    df = pd.DataFrame()
    
    for category, cat_id in sorted(category_to_id.items()):
        features_chi2 = chi2(features, labels == cat_id)
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(vectorizer.get_feature_names())[indices]
        max_ngram = max([len(f.split(' ')) for f in feature_names])

        sr = pd.Series(dtype=object)        
        
        for i in range(1, max_ngram+1):
            ngrams = [v for v in feature_names if len(v.split(' ')) == i]
            sr[f'{i}-grams'] = ngrams[-top_n_tokens:]

        df[category] = sr
        
    return df.T

def predict_text(text, classifier, vectorizer):
    """
    Returns predicted label of `text` based on `classifier` and `vectorizer`.
    """
    return {'text': text, 'prediction': classifier.predict(vectorizer.transform([text]))[0]}

def predict_text_label(text, model, tfidf, id_to_category):
    """
    Returns predicted label of `text` based on `classifier` and `vectorizer`.
    """
    return {'text': text, 'prediction': id_to_category[model.predict(tfidf.transform([text]))[0]]}

def train_text_classifier(df:pd.DataFrame, text_column:str, target_column:str, classifier):
    """
    Returns fitted vectorizer and classifier based on df DataFrame.
    - df: DataFrame for training
    - text_column: column name with text values to be used as features
    - target_column: column name of dependent variable to be predicted
    - classifier: classifier model to be used
    """
    X_train, X_test, y_train, y_test = train_test_split(df[text_column], df[target_column], random_state = 0)
    count_vect = CountVectorizer(ngram_range=(1,3))
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = classifier().fit(X_train_tfidf, y_train)
    return count_vect, clf

def compare_models(classifiers:list, features:np.array, labels:pd.Series, cv:int=5, scoring:str='accuracy'):
    """
    Plots chart comparing models based on cross validation method.
    - classifiers: list of classifiers to be compared
    - features: numpy array of text features (result of vectorizer)
    - labels: pandas Seires with target labels factorized (numeric values)
    - scoring: scoring metric, default is `accuracy`
    """
    
    entries = []
    for model in tqdm(classifiers):
        model_name = model.__class__.__name__
        scores = cross_val_score(model, features, labels, scoring=scoring, cv=cv)
        for fold_idx, score in enumerate(scores):
            entries.append((model_name, fold_idx, score))
    cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', scoring])
    sns.boxplot(x='model_name', y=scoring, data=cv_df)
    sns.stripplot(x='model_name', y=scoring, data=cv_df, 
                  size=8, jitter=True, edgecolor="gray", linewidth=2)

    plt.title('Model Comparison')
    plt.show()

    return cv_df

def plot_prediction_mistakes(df:pd.DataFrame, y_pred:pd.Series, y_test:pd.Series, category_to_id:dict, conf_mat:np.ndarray, indices_test:pd.Index, top_n_results:int=2):
    pd.options.display.max_colwidth=300
    
    for predicted in category_to_id.keys():
        for actual in category_to_id.keys():
            if predicted != actual and conf_mat[actual, predicted] >= 10:
                print("'{}' predicted as '{}' : {} examples.".format(category_to_id[actual], category_to_id[predicted], conf_mat[actual, predicted]))
                display(df.loc[indices_test[(y_test == actual) & (y_pred == predicted)]][['news_desk', 'abstract']].head(top_n_results))
                print('')
