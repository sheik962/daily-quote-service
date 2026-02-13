import boto3
import os
import json
import uuid
import random
from datetime import datetime
from botocore.exceptions import ClientError

# Configuration - moved inside to ensure region is applied
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'DailyMotivationalQuotes')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-2')

# Initialize resource with the specified region
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Success is not final, failure is not fatal... - Winston Churchill"
]

def store_quote_in_dynamodb(quote_id, quote, sent_date):
    try:
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'QuoteID': quote_id,
            'SentDate': sent_date,
            'Quote': quote,
            'Timestamp': datetime.now().isoformat()
        })
        print(f"✓ Quote stored: {quote_id}")
        return True
    except ClientError as e:
        print(f"✗ AWS Error: {e.response['Error']['Message']}")
        raise

def main(event=None, context=None): # Added params for Lambda compatibility
    try:
        quote_id = str(uuid.uuid4())
        quote = random.choice(QUOTES)
        sent_date = datetime.now().strftime('%Y-%m-%d')
        
        store_quote_in_dynamodb(quote_id, quote, sent_date)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'quoteId': quote_id, 'quote': quote})
        }
    except Exception as e:
        print(f"✗ Fatal Error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}

if __name__ == '__main__':
    main()
