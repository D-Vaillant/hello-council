# hello-council
An extremely simple script that uses `council-ai` as a wrapper to ChatGPT. Writes an `LLMCaller` call to encapsulate all of the council logic into a simple, easy-to-use chatbot without any memory. Basically just calling `CURL` to the API.

## Installation
You'll need `council-ai`:

`pip install council-ai`

Then just run `chat.py`. 

### Usage
```
david@Kenez hello_council % python chat.py "Can dogs play basketball?"
Asking...
No, dogs cannot play basketball.
```
