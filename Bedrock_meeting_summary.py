import boto3
import botocore.config
import json
import base64
from datetime import datetime
from email import message_from_bytes
from urllib.parse import parse_qs


# Function to extract plain text from a multipart email message
def extract_text_from_multipart(data):
    msg = message_from_bytes(data)  # Parse the email content into a message object

    text_content = ''  # Initialize variable to hold extracted text

    # Check if the email is multipart (contains multiple parts like attachments, text, etc.)
    if msg.is_multipart():
        for part in msg.walk():
            # Only extract plain text parts
            if part.get_content_type() == "text/plain":
                # Decode and add text content
                text_content += part.get_payload(decode=True).decode('utf-8') + "\n"
    else:
        # For single-part emails, extract if it's plain text
        if msg.get_content_type() == "text/plain":
            text_content = msg.get_payload(decode=True).decode('utf-8')

    # Return the extracted text, trimmed of any extra whitespace
    return text_content.strip() if text_content else None


# Function to generate a summary using the Bedrock AI model
def generate_summary_from_bedrock(content: str) -> str:
    # Format the prompt for summarization
    prompt_text = f"""Human: Summarize the following meeting notes: {content}
    Assistant:"""

    # Define model parameters for summary generation
    body = {
        "prompt": prompt_text,
        "max_tokens_to_sample": 5000,
        "temperature": 0.1,
        "top_k": 250,
        "top_p": 0.2,
        "stop_sequences": ["\n\nHuman:"]
    }

    try:
        # Initialize the Bedrock client with the appropriate configuration
        bedrock = boto3.client("bedrock-runtime", region_name="us-east-1",
                               config=botocore.config.Config(read_timeout=300, retries={'max_attempts': 3}))

        # Invoke the Bedrock model for summarization
        response = bedrock.invoke_model(body=json.dumps(body), modelId="anthropic.claude-v2")

        # Process the response to get the summary text
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        summary = response_data["completion"].strip()  # Extract the generated summary

        return summary  # Return the generated summary

    except Exception as e:
        print(f"Error generating the summary: {e}")
        return ""  # Return empty string if an error occurs


# Function to save the generated summary to an S3 bucket
def save_summary_to_s3_bucket(summary, s3_bucket, s3_key):
    s3 = boto3.client('s3')  # Initialize the S3 client

    try:
        # Upload the summary text to the specified S3 bucket and key
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=summary)
        print("Summary saved to s3")

    except Exception as e:
        print("Error when saving the summary to s3")


# Other function definitions remain the same

# Main Lambda function handler
def lambda_handler(event, context):
    # Decode the base64-encoded email body received in the event
    decoded_body = base64.b64decode(event['body'])

    # Extract plain text content from the email
    text_content = extract_text_from_multipart(decoded_body)

    # If no content could be extracted, return a 400 error response
    if not text_content:
        return {
            'statusCode': 400,
            'body': json.dumps("Failed to extract content")
        }

    # Generate a summary from the extracted content
    summary = generate_summary_from_bedrock(text_content)

    if summary:
        # Generate a unique S3 key with a timestamp for the summary file
        current_time = datetime.now().strftime('%H%M%S')  # UTC time
        s3_key = f'summary-output/meeting on {current_time}.txt'
        s3_bucket = 'bedrock-meeting-summarization'

        # Save the generated summary to the S3 bucket
        save_summary_to_s3_bucket(summary, s3_bucket, s3_key)

    else:
        print("No summary was generated")  # Log if no summary was created

    # Return a success response after processing
    return {
        'statusCode': 200,
        'body': json.dumps("Summary generation finished")
    }