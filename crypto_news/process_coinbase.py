import pandas as pd

def process_coinbase(file_path: str) -> pd.DataFrame:
    # Load the data from the CSV file
    coinbase = pd.read_excel(file_path)

    # Drop the null values
    coinbase = coinbase.dropna(subset=['ID', 'News'])

    # Drop if News is ' '
    coinbase = coinbase[coinbase['News'] != ' ']

    # conver the Date column to datetime
    coinbase['Date'] = pd.to_datetime(coinbase['Date'])

    # set the Date column as the index
    coinbase = coinbase.set_index('Date')

    coinbase = coinbase[['ID', 'News']]
    coinbase.drop_duplicates(subset=['ID', 'News'], inplace=True)

    # turn all News to lowercase
    coinbase['News'] = coinbase['News'].str.lower()

    # only keep row if bitcoin or btc is in string
    coinbase = coinbase[coinbase['News'].str.contains('bitcoin|btc')]

    # Return the dataframe
    return coinbase

if __name__ == '__main__':
    # Define the file path
    file_path = r'/Users/rakeenrouf/Downloads/Coinbase_new_2021_04_14_to_2024_03_20.xlsx'

    # Process the data
    coinbase_df = process_coinbase(file_path)

    # save the data to a csv file
    coinbase_df.to_csv('crypto_news/bitcoin.csv')

    # Display the first few rows of the dataframe
    print(coinbase_df.head())