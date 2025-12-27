from google import genai
from google.genai import types
import PIL.Image
import io
from config import Config

class geminiimgagent:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
    def generate_content(self, prompt,imagepath1,imagepath2):
        img1 = PIL.Image.open(imagepath1)
        img2 = PIL.Image.open(imagepath2)
        
        config = types.GenerateContentConfig(
            system_instruction="You are an memer. Add a more humorous/Dark  meme caption to this image. Do not change the background"
        )
        
        response = self.client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=[prompt, img1,img2],
            config=config
        )        
        
        for part in response.candidates[0].content.parts:
          if part.inline_data:
              img_data = io.BytesIO(part.inline_data.data)
              output_image = PIL.Image.open(img_data)
              output_image.save("transformed_output.png")
              print("✅ Image generated successfully! image name:-->transformed_output.png")

if __name__ == "__main__":
    image_path1 = r"./image_path1"    #provide the path of image_path1
    image_path2 = r"./image_path2"    #provide the path of image_path2
    Text="Michael Scott yelling 'No God Please No!' about weekend work."
    prompt=f"""Take this provided images and transform it into a standard internet meme by adding text overlay.
    Text content :{Text}
    1.Based provided images img1 img2 pick the best images form it which is prefectly suits form the {Text}
    2.understand the image and change the {Text} accordingly but not change the orginal meaning of the Text
    3.Overlay the text onto the image using the classic 'Impact' font style—bold, all-caps, white letters with a thick black outline.
    4.Placement: Position the text as a [Top/Bottom/Split] caption to maximize humor and visibility without covering the main subject's face
    5.Layout: If the text is long, split it into a setup at the top and a punchline at the bottom.
    6.Output: Return ONLY the final generated image with the text baked in. Do not change the original image's resolution or core content
    
    """
    agent = geminiimgagent()
    agent.generate_content(prompt,image_path1,image_path2)