import os
from openai import AzureOpenAI

endpoint = "https://ginge-mac10f7n-eastus2.cognitiveservices.azure.com/"
model_name = "o3-mini"
deployment = "o3-mini"

subscription_key = "AmFZuaTGrztL25vymqftEVD6qMvpYtCdZpW07FW5pPWZ2C7YzVeBJQQJ99BEACHYHv6XJ3w3AAAAACOGvxnP"
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant of selecint the food that I will eat.",
        },
        {
            "role": "user",
            "content": "I am hungry, what should I eat",
        }
    ],
    max_completion_tokens=100000,
    model=deployment
)

print(response.choices[0].message.content)