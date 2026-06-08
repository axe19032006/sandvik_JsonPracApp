from anthropic import AnthropicFoundry
import streamlit as st

base_url = st.secrets["AZURE_FOUNDRY_BASE_URL"]
api_key = st.secrets["AZURE_FOUNDRY_API_KEY"]
deployment = st.secrets["AZURE_FOUNDRY_DEPLOYMENT"]

# DEBUG: print what we're reading
print("Base URL:", repr(base_url))
print("Deployment:", repr(deployment))
print("API key (first 10 chars):", api_key[:10])

client = AnthropicFoundry(api_key=api_key, base_url=base_url)

message = client.messages.create(
    model=deployment,
    max_tokens=10000,
    messages=[{"role": "user", "content": "What is mining?"}]
)

print(message.content[0].text)