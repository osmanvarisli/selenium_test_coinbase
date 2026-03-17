import pandas as pd

def sorgula(market_df, main_df, exclude_market=None, include_market=None):
    """
    Filters the main dataframe based on market presence.
    """
    temp_df = main_df.copy().reset_index()
    
    # 1. Get list of coins that ARE on the excluded market
    if exclude_market:
        coins_to_exclude = market_df[market_df['Market'] == exclude_market]['Coin'].unique()
        temp_df = temp_df[~temp_df['Coin'].isin(coins_to_exclude)]
        
    # 2. Get list of coins that ARE on the required market
    if include_market:
        coins_to_include = market_df[market_df['Market'] == include_market]['Coin'].unique()
        temp_df = temp_df[temp_df['Coin'].isin(coins_to_include)]
        
    return temp_df

# --- Data Loading ---
# Using index_col=0 replaces the .set_index('Unnamed: 0') line
df = pd.read_csv('Market_degerleri.csv', index_col=0)
df2 = pd.read_csv('sss.csv', index_col='No')

# --- Market Analysis ---
df3 = df.groupby(['Coin', 'Total_Supply']).count()
df3 = df3.sort_values(by='Market', ascending=False)

# --- Pricing & Supply Filters ---
df2['Price'] = pd.to_numeric(df2['Price'], errors='coerce')
df2 = df2[df2['Circulating Supply'] < 50_000_000]

# Calculate Market Cap (s)
df2['s'] = df2['Price'] * df2['Circulating Supply']
df2 = df2.sort_values(by='s', ascending=False)

# --- Merging & Final Filtering ---
# Joining market counts with price data
ddff = df3.join(df2.set_index('Name'), on='Coin')

# Criteria
ddff = ddff[
    (ddff.Market > 20) & 
    (ddff.Price < 15) & 
    (ddff.Price > 0.005)
]

# --- Market Specific Filtering ---
# Example: Find coins NOT on Binance but meet all other criteria
exclude = ''         # Set to 'Binance' to hide Binance coins
include = 'Binance'  # Set to 'Binance' to only show Binance coins

final_results = sorgula(df, ddff, exclude_market=exclude, include_market=include)

# --- Output ---
print(final_results[['Coin', 'Symbol', 'Market', 'Price', 'Circulating Supply', 's']].head(50))
