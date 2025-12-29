import streamlit as st
import os
from meme_generator import geminiAgent
from vector_conversion import MemeSearchEngine
from agent2 import geminiimgagent


class Chatbot:
    def __init__(self):
        self.agent = geminiAgent()
        self.img_path = None


    def image_generation(self, userinput):
        try:
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
                
            agent.generate_image(userinput, images_path[0], images_path[1])
            self.img_path = "./transformed_output.png"
            return True
        except Exception as e:
                print(f"Fatal error: {str(e)}")
                return False

    def show_image(self, img_path):
        if img_path and os.path.exists(img_path):
            st.image(img_path, caption="My picture")
        else:
            st.error("Image file not found. Please check the file path.")

    def render_messages(self):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                if msg["type"] == "image":
                    if msg["content"] and os.path.exists(msg["content"]):
                        st.image(msg["content"], use_container_width=True)
                else:
                    st.write(msg["content"])

    def run(self,user_input):
        st.title("meme generation-Chatbot")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        self.render_messages()
        if user_input:
            st.session_state.messages.append({
                "role": "user",
                "type": "text",
                "content": user_input
            })
            st.session_state.messages.append({
                "role": "assistant",
                "type": "image",
                "content": self.img_path
            })

            with st.chat_message("user"):
                st.write(user_input)

            st.write("Here are some images for you")
            if self.image_generation(user_input):
                self.show_image(self.img_path)
                st.success("Image generated successfully!")
            else:
                st.error("Failed to generate image. Please try again.")


if __name__ == "__main__":
    chatbot = Chatbot()
    user_input = st.chat_input("what's on your mind?")
    chatbot.run(user_input)
