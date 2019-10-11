import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt


def parse_csv(files: list) -> dict:
    '''Parses a list of csv files into dict

    Parameters:
        files: list
        The list of files to be parsed
    '''
    dataframes = dict()

    for file in files:
        df = pd.read_csv(f'{file}.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        dataframes.update(
            {
                file: df
            }
        )

    return dataframes


def get_common_date(dataframes: dict) -> list:
    '''Gets range of common date from dataframes

    Parameters:
        dataframes: dict
        The dataframes to get the common date from
    '''
    common_date = list()

    for df in dataframes:
        df = dataframes[df]
        min_date = df.index.min()
        max_date = df.index.max()

        common_date.append([min_date, max_date])

    return common_date


def main():
    files = ['bitcoin_price', 'ethereum_price', 'litecoin_price', 'dash_price']
    legends = ['Bitcoin', 'Ethereum', 'Litecoin', 'Dash']

    dataframes = parse_csv(files)
    # zipping all min and max into two different tuples
    common_date = list(zip(*get_common_date(dataframes)))
    # unpacking values
    common_min, common_max = max(common_date[0]), min(common_date[1])

    # plotting the dataframes
    for crypto, legend in zip(files, legends):
        dataframes[crypto].sort_index(inplace=True)
        dataframes[crypto] = dataframes[crypto][common_min:common_max]

        dataframes[crypto]['Open'].dropna().plot(label=legend)
    
    # some matplotlib configs
    plt.title('Abertura (por dia) de criptomoedas em dólares')
    plt.xlabel('Anos')
    plt.ylabel('USD')
    plt.legend()

    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
