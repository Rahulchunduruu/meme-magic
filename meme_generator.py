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
            prompt = f"""Analyze the intent behind: '{userinput}'. 
            Generate a witty, relatable meme description under 15 words. 
            Provide the text only, no intro or outro."""
            
            response = self.gemini_llm.invoke([HumanMessage(content=prompt)])
            return response.content
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
                        1.Based provided images img1 img2 pick the best images form it which is prefectly suits form the {userinput} and don't overlay one image on other image
                        2.understand the image and change the {userinput} accordingly but not change the orginal meaning of the Text
                        3.Overlay the text onto the image using the classic 'Impact' font style—bold, all-caps, white letters with a thick black outline.
                        4.Placement: Position the text as a [Top/Bottom/Split] caption to maximize humor and visibility without covering the main subject's face
                        5.Layout: If the text is long, split it into a setup at the top and a punchline at the bottom.
                        6.Output:Do not change the original image's resolution or core content
                        """
            img = geminiimgagent()
            img.generate_content(userinput, imagepath1, imagepath2)
        except ResourceExhausted:
            print(" API quota exceeded for image generation.")
        except Exception as e:
            print(f"Error generating image: {str(e)}")


if __name__ == "__main__":
    try:
        #generating the humar text
        #userinput = 'i have a driving licence but i am blind police be like....'
        userinput = "i love dogs but i dont feed dogs beacuse i love to eat dogs"
        agent = geminiAgent()
        response = agent.generate_response(userinput)
        if not response:
            print("Failed to generate meme description")
            rep()
            
        print(f"gemini Response: {response}")
        
        #find the images
        engine = MemeSearchEngine()
        results = engine.find_best_meme(response)
        
        #image generation
        images_path = [result['image'] for result in results[:2]]
        print("selected images are give to the model")
        
        agent.generate_image(userinput, images_path[0], images_path[1])
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
