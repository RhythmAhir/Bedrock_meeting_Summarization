# Project Report: Meeting Summary Generation System with AWS Lambda, Bedrock, API Gateway, and Amazon S3

---

## 1. **Introduction**

In this project, I built a serverless system that automatically generates summaries from large documents, such as meeting notes, using **AWS Lambda** and **AWS Bedrock**. For this implementation, I used the **"Anthropic Claude-v2"** model from Bedrock to summarize meeting content. The system is designed to process email content containing meeting notes, extract the relevant text, generate a summary, and store the result in an **S3 bucket**. The system is accessed via **API Gateway**, allowing users to easily submit documents for summarization.

As a test, I used a sample document: the **US Chemical Safety Board meeting minutes from January 20, 2016**, which is 27 pages long. This document was uploaded into the system for summarization, showcasing the system’s ability to handle large amounts of text and produce concise summaries.

---

## 2. **Creating the AWS Lambda Function**

The AWS Lambda function serves as the core of my summary generation process. It extracts plain text from multipart emails, generates a Bedrock summary, and saves the result in an S3 bucket.

### Lambda Code Overview

- **Text Extraction**:  
  I used the `extract_text_from_multipart` function to parse incoming email content, decoding and extracting the plain text sections used as input for the summary generation.
  
- **Summary Generation with Bedrock**:  
  I implemented the `generate_summary_from_bedrock` function to construct a prompt based on the extracted content, specifying that the text should be summarized. This prompt is sent to Bedrock’s **"Anthropic Claude-v2"** model, with parameters like `temperature`, `max_tokens_to_sample`, `top_k`, and `top_p` configured to control the response quality.
  
- **Storing Summary in S3**:  
  I used the `save_summary_to_s3_bucket` function to store the generated summary in a specified **S3 bucket** with a unique key. Each summary is saved in the `summary-output` folder within the bucket, using a timestamped filename for easy tracking and retrieval.

- **Lambda Handler**:  
  I set up the `lambda_handler` function to decode the email content, extract text, generate a summary, and save the output in S3. The handler returns a successful response to API Gateway.

The complete code for this Lambda function can be found in the **"Bedrock_meeting_summary.py"** file.

**Screenshot of the Lambda function code configuration**:  

![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/1.%20Lambda%20Function.png>)

---

## 3. **Configuring Amazon S3 for Summary Storage**

I created an S3 bucket named `bedrock-meeting-summarization` to store the output summaries. Each generated summary is saved with a unique timestamped filename under the `summary-output` folder, allowing for easy tracking and retrieval.

**Screenshot of the S3 bucket configuration**:  

![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/2.%20Meeting_summary%20S3%20Bucket%20Created.png>)

---

## 4. **Setting Up API Gateway for External Access**

I configured **API Gateway** to enable external access to the Lambda function, allowing users to submit email content for summarization via HTTP POST. The setup includes:

1. **Integration with Lambda**:  
   The API Gateway is integrated with the Lambda function, which triggers the summarization process upon receiving a request.

2. **Defining Routes**:  
   I created a POST route (`/meeting-summary`) in API Gateway, which directs incoming requests to the Lambda function for processing.

**Screenshots of API Gateway integration and route configuration**:  

![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/3.%20Meeting_Summary%20API%20Gateway%20Integration%20with%20Lambda%20Function.png>)

![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/4.%20API%20Gateway%20Route.png>)

---

## 5. **Testing the API with Postman**

To test the system, I uploaded an entire **27-page US Chemical Safety Board meeting document from January 20, 2016**. This document, containing meeting notes, was used to demonstrate the summarization capabilities of the Lambda function.

1. **Postman Request**:  
   I submitted the document as a base64-encoded file through a **POST** request to the **API Gateway**. The file was sent with a JSON payload, specifying the key `meeting-summary-01` and containing the content to be summarized.
   
2. **API Response**:  
   The Lambda function processed the document and generated a summary. The system returned a successful response, confirming the completion of the summary generation. The summarized content was then stored in the **S3 bucket** for future access.

**Screenshot of the Postman request and response confirming successful execution**:  

![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/5.%20POSTMAN%20POST.png>)

---

## 6. **Verifying Output in S3 Bucket**

After executing the Lambda function, I verified that the generated summary was saved in the S3 bucket `bedrock-meeting-summarization` under the `summary-output` folder. The unique timestamped filename confirmed successful storage.

**Screenshot of the generated summary file in the S3 bucket**:  

![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/6.%20File%20Generated%20In%20S3.png>)

---

## 7. **Viewing the Generated Summary**

Here is an example of the generated summary based on the meeting notes provided in the request. This summary was created using Bedrock's capabilities and saved in the S3 bucket for future reference.

**Screenshot of the generated summary content**:  

![Alt text](<https://github.com/RhythmAhir/Bedrock_meeting_Summarization/blob/main/Screenshot/7.%20Output%20Summary.png>)

---

## Conclusion

This project successfully demonstrates my ability to integrate **AWS Lambda**, **Bedrock's "Anthropic Claude-v2"**, **API Gateway**, and **Amazon S3** to build a serverless, automated summarization API. The structured configuration allows users to submit meeting notes as email content, which the system processes to generate and save summaries for easy retrieval. This solution provides a scalable foundation for similar text-processing applications, offering a streamlined approach to content summarization and storage.
