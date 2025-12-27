# Meme Generator with Gemini AI

An intelligent meme generator that uses Google's Gemini AI to analyze user queries, find matching memes, and generate new memes with custom captions.

## Features

- **Query Understanding**: Uses Gemini LLM to understand user input and generate meme descriptions
- **Meme Search**: Finds best matching memes from database using vector similarity
- **Meme Generation**: Generates new memes with AI-powered captions using Gemini vision models
- **Image Processing**: Adds text overlays with Impact font styling
- **Error Handling**: Comprehensive exception handling for API errors and edge cases

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
GEMINI_API_KEY1=backup_key_1
GEMINI_API_KEY2=backup_key_2
GEMINI_API_KEY3=backup_key_3
```

Get your API key from: https://console.cloud.google.com/apis/credentials

## Usage

### Basic Usage
```python
from meme_generator import geminiAgent

agent = geminiAgent()
userinput = 'i dont like to work on weekend'
response = agent.generate_response(userinput)
print(f"Meme description: {response}")
```

### Generate Meme with Images
```python
agent.generate_image(userinput, image_path1, image_path2)
```

## Error Handling

The application handles the following exceptions:

- **ResourceExhausted**: API quota exceeded - use backup API keys or wait
- **GoogleAPIError**: General API errors with detailed messages
- **Missing Data**: Validates image paths and meme search results
- **Network Errors**: Catches connection issues gracefully

All errors are logged with user-friendly messages.

## Files

- **agent2.py**: `geminiimgagent` class for generating memes with Gemini
- **meme_generator.py**: `geminiAgent` class for understanding queries and orchestrating meme generation
- **vector_conversion.py**: `MemeSearchEngine` for finding similar memes
- **config.py**: Configuration loader for API keys

## Notes

- Suppress warnings: `warnings.filterwarnings('ignore')`
- Free tier has rate limits - use backup API keys if quota exceeded
- Generated memes saved as `transformed_output.png`
- Check console output for error messages and status updates
