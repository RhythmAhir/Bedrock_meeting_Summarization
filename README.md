# Project Report: Meeting Summary Generation System with AWS Lambda, Bedrock, API Gateway, and Amazon S3

## 1. **Introduction**

This project involves creating a serverless system to generate meeting summaries from email content. Using **AWS Lambda** as the processing engine, the system integrates with **AWS Bedrock** to utilize the foundational model **Anthropic Claude-v2** for summarization. The system is accessible through **API Gateway**, allowing users to submit requests via **Postman**, and the generated summary is saved in an **S3 bucket** for easy access and storage.

---

## 2. **Creating the AWS Lambda Function**

The AWS Lambda function is the core of the summary generation process. It extracts plain text from multipart emails, generates a Bedrock summary, and saves the result in an S3 bucket.

### Lambda Code Overview

- **Text Extraction**: 
  - The `extract_text_from_multipart` function parses the incoming email content, decoding and extracting the plain text sections used as input for the summary generation.
  
- **Summary Generation with Bedrock**:
  - The `generate_summary_from_bedrock` function constructs a prompt based on the extracted content, specifying that the text should be summarized. This prompt is sent to Bedrock’s **"AnthBedrock'sude"v2"** model, and pa"ameters like `temperature,` `max_tokens_to_sample,` `top_k,` and `top_p` are configured to control the response quality.
  
- **Storing Summary in S3**:
  - The `save_summary_to_s3_bucket` function stores the generated summary in a specified **S3 bucket** with a unique key. Each summary is saved in the `summary-output` folder within the bucket, using a timestamped filename for easy tracking and retrieval.

- **Lambda Handler**:
  - The `lambda_handler` function decodes the email content, extracts text, generates a summary, and, if successful, saves the output in S3. The handler returns a successful response to API Gateway.

The complete code for this Lambda function can be found in the **"Bedrock_meeting_summary.py"** file.

**Screenshot of the Lambda function code configuration**:  
![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/1.%20Lambda%20Function.png>)

---

## 3. **Configuring Amazon S3 for Summary Storage**

An S3 bucket named `bedrock-meeting-summarization` was created to store the output summaries. Each generated summary is saved with a unique timestamped filename under the `summary-output` folder, allowing easy tracking and retrieval.

**Screenshot of the S3 bucket configuration**:  
![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/2.%20Meeting_summary%20S3%20Bucket%20Created.png>)

---

## 4. **Setting Up API Gateway for External Access**

**API Gateway** was configured to enable external access to the Lambda function, allowing users to submit email content for summarization via HTTP POST. The setup includes:

1. **Integration with Lambda**:
   - The API Gateway is integrated with the Lambda function, which triggers the summarization process upon receiving a request.

2. **Defining Routes**:
   - A POST route (`/meeting-summary`) was created in API Gateway, which directs incoming requests to the Lambda function for processing.

**Screenshots of API Gateway integration and route configuration**:  
![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/3.%20Meeting_Summary%20API%20Gateway%20Integration%20with%20Lambda%20Function.png>)
![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/4.%20API%20Gateway%20Route.png>)

---

## 5. **Testing the API with Postman**

To verify the setup, we tested the API using **Postman**. A POST request was sent with a file containing the meeting notes to be summarized.

1. **Postman Request**:
   - The request includes a JSON payload with the base64-encoded email content.
   
2. **API Response**:
   - A successful response from the API confirmed that the Lambda function executed as expected, generating the summary and saving it in S3.

**Screenshot of the Postman request and response confirming successful execution**:  
![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/5.%20POSTMAN%20POST.png>)

---

## 6. **Verifying Output in S3 Bucket**

After executing the Lambda function, the generated summary was saved in the S3 bucket `bedrock-meeting-summarization` under the `summary-output` folder. The unique timestamped filename confirmed successful storage.

**Screenshot of the generated summary file in the S3 bucket**:  
![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/6.%20File%20Generated%20In%20S3.png>)

---

## 7. **Viewing the Generated Summary**

Here is an example of the generated summary based on the meeting notes provided in the request. This summary was created using Bedrock's summariBedrock'spabilities and saved in the S3 bucket for future reference.

**Screenshot of the generated summary content**:  
![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/7.%20Output%20Summary.png>)

---

## Conclusion

This project successfully demonstrates the integration of **AWS Lambda**, **Bedrock’s "AnthroBedrock'se"v2" model**, **API "ateway**, and **Amazon S3** to build a serverless, automated summarization API. The structured configuration allows users to submit meeting notes as email content, which the system processes to generate saved summaries for easy retrieval. This solution is a scalable foundation for similar text-processing applications, providing a streamlined content summarization and storage approach.
