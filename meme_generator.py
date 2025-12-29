from vector_conversion import MemeSearchEngine
from config import Config
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage
from google.api_core.exceptions import GoogleAPIError, TooManyRequests, ResourceExhausted
from agent2 import geminiimgagent
import warnings
warnings.filterwarnings('ignore')


class geminiAgent:
    def __init__(self):
        'initialize Gemini LLM for meme search'
        self.gemini_llm = ChatGoogleGenerativeAI(
            api_key=Config.GEMINI_API_KEY,
            model="gemini-2.5-flash",
            temperature=1.7,
            max_tokens=500
        )

    def generate_response(self, userinput: str) -> str:
        'generate response using Gemini LLM'
        try:
            #prompt = f"Meme caption for: {userinput}"
            
            prompt =f"""You are a meme template selection engine.

                    Your task is to analyze the input text and generate keywords and signals that help choose the BEST meme template from a meme template database.

                    Think in terms of:
                    - Reaction memes
                    - Situation-based memes
                    - Emotion exaggeration
                    - Relatable internet humor

                    Rules:
                    1. Identify the PRIMARY emotion (mandatory).
                    2. Identify the INTENSITY of the emotion (low, medium, high).
                    3. Identify the SITUATION type (failure, success, confusion, sarcasm, flex, irony, shock, expectation vs reality, etc.).
                    4. Infer the most suitable MEME REACTION STYLE (facepalm, smug, crying, shocked, deadpan, celebration, awkward).
                    5. Convert everything into SHORT, SEARCHABLE meme keywords.
                    6. Avoid full sentences.
                    7. Output in structured format ONLY.
                    8.Strictly limit your entire response to 20 words or fewer

                    Input text:
                    "{userinput}"

                    Output format:
                    emotion: <emotion>
                    intensity: <low|medium|high>
                    situation: <situation-type>
                    reaction_style: <reaction-type>
                    keywords: keyword1, keyword2, keyword3, keyword4, keyword5
                """
            
            response = self.gemini_llm.invoke([HumanMessage(content=prompt)])
            #text = response.content.strip().split('\n')[0]
            return response.content.strip()
        except ResourceExhausted:
            print(" API quota exceeded. Please try again later or use a different API key.")
            return None
        except GoogleAPIError as e:
            print(f" API Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None
    
    def generate_image(self, userinput: str, imagepath1, imagepath2) -> str:
        try:
            if not imagepath1 or not imagepath2:
                print("Error: Image paths not provided")
                return None

            prompt = f"""Take this provided image and transform it into a standard internet meme by adding userinput overlay.
                        Text content :{userinput}
                        IMAGES : {imagepath1}{imagepath2}
                        1.Based provided IMAGES pick the best one images form it which is prefectly suits form the Text content and don't overlay one image on other image
                        2.understand the IMAGES and change the Text content text accordingly but not change the orginal meaning of the Text
                        3.Overlay the text onto the image using the classic 'Impact' font style—bold, all-caps, white letters with a thick black outline.
                        4.Placement: Position the text as a [Top/Bottom/Split] caption to maximize humor and visibility without covering the main subject's face
                        5.Layout: If the text is long, split it into a setup at the top/sideup/bottomleft/top left and a punchline at the bottom./sidedown/bottomright/top down
                        """
            img = geminiimgagent()
            img.generate_content(prompt, imagepath1, imagepath2)
        except ResourceExhausted:
            print(" API quota exceeded for image generation.")
        except Exception as e:
            print(f"Error generating image: {str(e)}")


if __name__ == "__main__":
    try:
        #generating the humar text
        #userinput = 'i have a driving licence but i am blind police be like....'
        #serinput = "i love coffee at late night beacause of that i have a sleeping issue"
        userinput = "i know how to drive bike but i am blind"
        agent = geminiAgent()
        response = agent.generate_response(userinput)
        if not response:
            print("Failed to generate meme description")
            exit()
            
        print(f"gemini Response: {response}")
        
        #find the images
        engine = MemeSearchEngine()
        results = engine.find_best_meme(response)
        
        #image generation
        images_path = [result['image'] for result in results[:2]]
        print("selected images are give to the model")
        
        print("images are here",*images_path)
        agent.generate_image(userinput, images_path[0], images_path[1])
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
