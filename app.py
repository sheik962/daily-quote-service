
import boto3
import os
import json
from datetime import datetime
import uuid
import random

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')

# Configuration
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'DailyMotivationalQuotes')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-2')

# Sample motivational quotes
QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. - Confucius",
    "Start where you are. Use what you have. Do what you can. - Arthur Ashe",
    "The only impossible journey is the one you never begin. - Tony Robbins",
    "Everything you've ever wanted is on the other side of fear. - George Addair"
]

def get_random_quote():
    """Select a random motivational quote"""
    return random.choice(QUOTES)

def store_quote_in_dynamodb(quote_id, quote, sent_date):
    """Store the quote in DynamoDB table"""
    try:
        table = dynamodb.Table(TABLE_NAME)
        
        item = {
            'QuoteID': quote_id,
            'SentDate': sent_date,
            'Quote': quote,
            'Timestamp': datetime.now().isoformat()
        }
        
        table.put_item(Item=item)
        print(f"✓ Quote stored successfully in DynamoDB")
        print(f"  QuoteID: {quote_id}")
        print(f"  SentDate: {sent_date}")
        print(f"  Quote: {quote}")
        return True
        
    except Exception as e:
        print(f"✗ Error storing quote in DynamoDB: {str(e)}")
        raise

def main():
    """Main function to generate and store quote"""
    try:
        print("=" * 60)
        print("Daily Motivational Quote Service - Starting")
        print("=" * 60)
        
        # Generate quote ID and get quote
        quote_id = str(uuid.uuid4())
        quote = get_random_quote()
        sent_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"
Generated Quote ID: {quote_id}")
        print(f"Date: {sent_date}")
        print(f"Quote: {quote}
")
        
        # Store in DynamoDB
        print("Storing quote in DynamoDB...")
        store_quote_in_dynamodb(quote_id, quote, sent_date)
        
        print("
" + "=" * 60)
        print("Process completed successfully!")
        print("=" * 60)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Success',
                'quoteId': quote_id,
                'quote': quote
            })
        }
        
    except Exception as e:
        print(f"
✗ Error in main process: {str(e)}")
        raise

if __name__ == '__main__':
    main()


