
from fastapi import FastAPI, Query
import pandas as pd 
import boto3 
from io import StringIO 
import uvicorn

app = FastAPI()
def fetch_data(year: int = None, country: str = None, market: str = None):

    try:
# Load CSV content into a pandas DataFrame from the S3 URL
        df = pd.read_csv("https://dataset-market.s3.us-east-1.amazonaws.com/total_data.csv")
        print(df.shape[0]) # Print the number of rows in the original DataFrame 
        if year is not None:
           print("Filtering by year")
           df = df[df['year'] == year]
        if country is not None:
            print("Filtering by country")
            df = df[df['country'] == country]
        if market is not None:
           print("Filtering by market")
           df = df[df['mkt_name'] == market]   
        df_filter = df.fillna('')
        print(df_filter.shape[0]) # Print the number of rows after filtering
# Convert filtered DataFrame to JSON
        if df_filter.empty:
            raise ValueError('No data found for the specified filters.')
# Raise error if no data found
        else:
           filtered_json = df_filter.to_json(orient='records')
           return filtered_json
    except Exception as e:
       return {'error': str(e)}
    
@app.get('/fetch_data') # Define an endpoint for the API
async def fetch_data_api(year: int = Query(None), country: str = Query(None), market: str = Query(None)):

    try:
      
      # Call fetch_data function with provided parameters
      filtered_data = fetch_data(year, country, market)
      if filtered_data is None:
        raise ValueError('No data found for the specified filters.')
      else:
       # Return filtered data as API response
        return filtered_data
    except Exception as e:
        return {'error': str(e)}, 400
if __name__ == "__main__":
# Run the FastAPI application using uvicorn server
   uvicorn.run(app, port=8080, host='0.0.0.0') 