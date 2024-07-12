import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


class h1_h2_returns:
    def __init__(self, ticker):
        self.ticker = ticker
    
    def get_data(self):
        data = yf.download(self.ticker, start="2009-01-01", end="2024-06-28", progress=False)
        return data['Close']
    
    def returns(self):
        data = self.get_data()

        # Define the specific dates you want to filter for
        specific_dates = ['01-01', '06-30', '07-01', '12-31']

        # Create a list to store the filtered data
        filtered_data = []

        # Loop through each year in the data
        for year in range(data.index.year.min(), data.index.year.max() + 1):
            for date in specific_dates:
                target_date = pd.Timestamp(f"{year}-{date}")

                if target_date in data.index:
                    filtered_data.append({
                        'date': target_date.date(),  # Convert to date
                        'price': data.loc[target_date]
                    })
                else:
                    closest_date = None

                    # Check both forward and backward for the closest trading date
                    for offset in range(1, 6):  # Check up to 5 days forward or backward
                        forward_date = target_date + pd.Timedelta(days=offset)
                        backward_date = target_date - pd.Timedelta(days=offset)
                        
                        if forward_date in data.index:
                            closest_date = forward_date
                            break
                        elif backward_date in data.index:
                            closest_date = backward_date
                            break

                    if closest_date:
                        filtered_data.append({
                            'date': closest_date.date(),  # Convert to date
                            'price': data.loc[closest_date]
                        })

        # Convert the list to a DataFrame
        filtered_data_df = pd.DataFrame(filtered_data)

        # Optionally set the 'date' column as the index
        filtered_data_df.set_index('date', inplace=True)

        result = []

        # Iterate over the index of filtered_data_df
        for i in range(0, len(filtered_data_df), 4):
            if i + 3 < len(filtered_data_df):  # Ensure there are enough rows to access
                year = filtered_data_df.index[i].year
                
                # Calculate first half return
                first_half_return = ((filtered_data_df['price'].iloc[i+1] / filtered_data_df['price'].iloc[i]) - 1) * 100
                
                # Calculate second half return
                second_half_return = ((filtered_data_df['price'].iloc[i+3] / filtered_data_df['price'].iloc[i+2]) - 1) * 100
                
                result.append({
                    'year': year,
                    'first_half_return': first_half_return,
                    'second_half_return': second_half_return
                })

        result_df = pd.DataFrame(result)
        
        return result_df
    
    def visualize(self):
        data = self.returns()

        # Create the bar chart
        plt.figure(figsize=(10, 6))

        # Plot the first half returns
        plt.bar(data['year'] - 0.2, data['first_half_return'], width=0.4, label='First Half Returns')

        # Plot the second half returns
        plt.bar(data['year'] + 0.2, data['second_half_return'], width=0.4, label='Second Half Returns')

        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('Returns (%)')
        plt.title('First Half vs. Second Half Returns')
        plt.xticks(data['year'])
        plt.legend()

        # Show the plot
        plt.show()