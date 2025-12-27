# Meme Generator Chatbot with Gemini AI

A Streamlit-based chatbot that generates memes using Google's Gemini AI. It analyzes user queries, finds matching memes, and creates new memes with custom captions.

## Features

- **Streamlit UI**: Interactive chat interface for meme generation
- **Query Understanding**: Gemini LLM generates meme descriptions from user input
- **Meme Search**: Vector-based search to find matching memes
- **Meme Generation**: AI-powered meme creation with text overlays
- **Error Handling**: Robust exception handling for API and file errors
- **Class-Based Architecture**: Clean OOP design with `Chatbot` class

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

Get your API key from: https://console.cloud.google.com/apis/credentials

## Usage

### Run Streamlit App
```bash
streamlit run app.py
```

Then type your meme idea in the chat input.

### Run from Terminal (Script Mode)
```bash
python meme_generator.py
```

Edit the `userinput` variable in the `__main__` section to change the meme prompt:
```python
userinput = "your meme idea here"
agent = geminiAgent()
response = agent.generate_response(userinput)
print(f"Meme caption: {response}")

engine = MemeSearchEngine()
results = engine.find_best_meme(response)
images_path = [result['image'] for result in results[:2]]

agent.generate_image(userinput, images_path[0], images_path[1])
```

Generated meme will be saved as `transformed_output.png`.

## Architecture

**Chatbot Class** (`app.py`):
- `image_generation()`: Orchestrates meme generation pipeline
- `show_image()`: Displays generated meme with file validation
- `render_messages()`: Renders chat history
- `run()`: Main app loop

**geminiAgent Class** (`meme_generator.py`):
- `generate_response()`: Creates meme caption from user input
- `generate_image()`: Generates meme image with text overlay

**geminiimgagent Class** (`agent2.py`):
- `generate_content()`: Calls Gemini vision API to create meme

**MemeSearchEngine Class** (`vector_conversion.py`):
- `find_best_meme()`: Finds matching memes using vector similarity

## Error Handling

- **Token Limit**: Prompts are optimized to stay within 77 token limit
- **File Not Found**: Validates image paths before display
- **API Quota**: Handles ResourceExhausted exceptions
- **Missing Data**: Checks for valid image paths and search results

## Generated Files

- `transformed_output.png`: Generated meme image
- `.gitignore`: Excludes cache, venv, and generated files

## Notes

- Generated memes saved as `transformed_output.png`
- Chat history stored in Streamlit session state
- Check console for error messages and status updates
