import torch
import faiss
import os
import pickle
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import warnings
warnings.filterwarnings('ignore')


class MemeSearchEngine:
    """A class to search memes using CLIP embeddings and FAISS indexing."""
    
    def __init__(self, meme_dir="memes database/", index_file="meme_index.faiss", paths_file="meme_paths.pkl"):
        """Initialize the MemeSearchEngine with model and configuration.ls
        
        
        Args:
            meme_dir: Directory containing meme images
            index_file: Path to save/load FAISS index
            paths_file: Path to save/load image paths
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.meme_dir = meme_dir
        self.index_file = index_file
        self.paths_file = paths_file
        self.dimension = 512
        self.index = None
        self.image_paths = []

    def image_to_vector(self, image_path):
        """Convert an image to a normalized vector embedding.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Normalized numpy array of image features
        """
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            features = self.model.get_image_features(**inputs)
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()[0]

    def text_to_vector(self, text):
        """Convert text to a normalized vector embedding.
        
        Args:
            text: Input text string
            
        Returns:
            Normalized numpy array of text features
        """
        inputs = self.processor(text=[text], return_tensors="pt").to(self.device)
        with torch.no_grad():
            features = self.model.get_text_features(**inputs)
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()[0]

    def build_index(self):
        """Build FAISS index from all images in meme directory and save to disk."""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.image_paths = []
        
        for file in os.listdir(self.meme_dir):
            if file.endswith((".jpg", ".png", ".jpeg")):
                path = os.path.join(self.meme_dir, file)
                if os.path.exists(path):
                    vector = self.image_to_vector(path)
                    self.index.add(vector.reshape(1, -1))
                    self.image_paths.append(path)
                else:
                    print("Skipping missing file:", path)
        
        faiss.write_index(self.index, self.index_file)
        with open(self.paths_file, "wb") as f:
            pickle.dump(self.image_paths, f)

    def load_index(self):
        """Load pre-built FAISS index and image paths from disk."""
        self.index = faiss.read_index(self.index_file)
        with open(self.paths_file, "rb") as f:
            self.image_paths = pickle.load(f)

    def find_best_meme(self, clr_text, top_k=2):
        """Find the best matching meme(s) for given text query.
        
        Args:
            user_text: Text query to search for
            top_k: Number of top results to return
            
        Returns:
            List of dicts with 'image' path and 'score' for each result
        """
        if self.index is None:
            self.load_index()
        
        query_vector = self.text_to_vector(clr_text)
        scores, indices = self.index.search(query_vector.reshape(1, -1), top_k)
        #print(scores, indices)
        results = []
        for i, score in zip(indices[0], scores[0]):
            results.append({
                "image": self.image_paths[i],
                "score": float(score)
            })
        return results


if __name__ == "__main__":
    engine = MemeSearchEngine()
    if not os.path.exists("meme_index.faiss") and not os.path.exists("meme_paths.pkl"):
        engine.build_index()
        print("Index built and saved.")
    
    print("searching started in the data base")
    query = "when your code works but you don't know why"
    results = engine.find_best_meme(query)
    print(results)
