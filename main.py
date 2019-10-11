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


def plot_data(dataframes: dict, common_min: str=None, common_max: str=None) -> None:
    '''Plots the DataFrames data from a dict

    Parameters:
        dataframes: dict
        The DataFrames to be plotted

        common_min: str
        Timestamp object from where to start plotting data
        Optional -> Defaults to: None

        common_max: str
        Timestamp object from where to end plotting data
        Optional -> Defaults to: None
    '''
    # zipping all min and max into two different tuples
    common_date = list(zip(*get_common_date(dataframes)))

    if not common_min:
        common_min = max(common_date[0])

    if not common_max:
        common_max = min(common_date[1])

    # plotting the dataframes
    for crypto, legend in zip(files, legends):
        dataframes[crypto].sort_index(inplace=True)
        dataframes[crypto] = dataframes[crypto][common_min:common_max]

        dataframes[crypto]['Open'].plot(label=legend, linewidth=1)
    
    # some matplotlib configs
    plt.style.use('seaborn-colorblind')

    plt.title('Abertura de criptomoedas em dólares ao longo dos anos')
    plt.xlabel('Anos')
    plt.ylabel('USD')
    plt.legend()

    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    global files, legends
    files = ['bitcoin_price', 'ethereum_price', 'litecoin_price', 'dash_price']
    legends = ['Bitcoin', 'Ethereum', 'Litecoin', 'Dash']

    dataframes = parse_csv(files)
    plot_data(dataframes)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
