import pandas as pd
import matplotlib.pyplot as plt

def process_bitcoin(file_path: str) -> pd.DataFrame:
    # Load the data from the CSV file
    bit_news = pd.read_csv(file_path)

    # convert the Date column to datetime
    bit_news['DateTime'] = pd.to_datetime(bit_news['Date'])

    # make a new column 'date' and only keep the day from the 'Date' column
    bit_news['date'] = bit_news['DateTime'].dt.date

    # set the 'date' column as the index
    bit_news = bit_news.set_index('date')

    # Return the dataframe
    return bit_news

def process_bitcoin_return(file_path: str) -> pd.DataFrame:
    # Load the data from the CSV file
    bit_news = pd.read_csv(file_path)

    # convert the Unnamed: 0 column to datetime
    bit_news['DateTime'] = pd.to_datetime(bit_news['Unnamed: 0'])

    # set the 'DateTime' column as the index
    bit_news = bit_news.set_index('DateTime')

    # Return the dataframe
    return bit_news


def sentiment_label(perc_return: float, vn=-4, n=0.3, p=4) -> str:
    """
    very negative: perc_return < -4
    negative: -4 <= perc_return < -0.3
    neutral: -0.3 <= perc_return < 0.3
    positive: 0.3 <= perc_return < 4
    very positive: perc_return >= 4
    """
    
    if perc_return < vn:
        return 'very negative'
    elif vn <= perc_return < -n:
        return 'negative'
    elif -n <= perc_return < n:
        return 'neutral'
    elif n <= perc_return < p:
        return 'positive'
    else:
        return 'very positive'

if __name__ == '__main__':
    # Define the file path for bitcoint returns
    file_path = r'yfinance_return/BTC_return.csv'

    # Process the data
    bit_return_df = process_bitcoin_return(file_path)

    # only keep Returns column
    bit_return_df = bit_return_df[['Returns']]

    # Define the file path for bitcoint news
    file_path = r'crypto_news/bitcoin.csv'

    # Process the data
    bit_news_df = process_bitcoin(file_path)


    # only keep ID and News columns
    bit_news_df = bit_news_df[['ID', 'News']]

    # group by index and join the news
    bit_news_df = bit_news_df.groupby(level=0).agg({'News': ' '.join})

    # make another version of this but where news is one day behind
    bit_news_df['News_lag'] = bit_news_df['News'].shift(1)

    df = bit_news_df.merge(bit_return_df, left_index=True, right_index=True, 
                           how='left')
    
    df['perc_return'] = df['Returns'] * 100
    df['label'] = df['perc_return'].apply(lambda x: sentiment_label(x))
    df = df[['label', 'News_lag', 'News', 'Returns', 'perc_return']]

    # Display the first few rows of the dataframe
    print(bit_news_df.head())

    # plot histogram of the label
    # df['label'].value_counts().plot(kind='bar')
    # # rotate the x-axis labels
    # plt.xticks(rotation=45)

    # plot histogram of the perc_return
    df['perc_return'].hist()

    # show the plot
    plt.show()

    # Save the dataframe to a CSV file
    df.to_csv(r'response_variable/bitcoin_news_return_label.csv')
