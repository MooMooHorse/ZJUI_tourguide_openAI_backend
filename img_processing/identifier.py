import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from paths import image_proc_dir, tagged_image_dir, img_checkpoint_dir, img_proc_dir
sys.path.append(img_proc_dir)
from speak import speak
from tqdm import tqdm


import cv2
import json
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib  # For saving the model

class ImageClassifier:
    def __init__(self, model_path=None):
        self.image_dir = Path(image_proc_dir)
        self.tagged_data_dir = Path(tagged_image_dir)
        self.features = []
        self.labels = []

        if model_path:
            print('model loaded' + f''' in path {model_path}''')
            self.model = joblib.load(model_path)
        else:
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def extract_features(self, image):
        # Resize the image to a standard size
        image = cv2.resize(image, (100, 100))
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # Use histogram of oriented gradients (HOG) as features
        winSize = (64, 64)
        blockSize = (16, 16)
        blockStride = (8, 8)
        cellSize = (8, 8)
        nbins = 9
        hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
        hog_features = hog.compute(gray_image)
        return hog_features.flatten()

    def load_data(self):
        # Load all json files and corresponding images
        print('loading data')
        for json_file in tqdm(self.tagged_data_dir.glob('*.json'), desc='Loading data'):
            with open(json_file, 'r') as f:
                data = json.load(f)
            image_path = self.image_dir / data['image_name']
            if image_path.exists():
                image = cv2.imread(str(image_path))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                features = self.extract_features(image)
                self.features.append(features)
                self.labels.append(data['category'])

    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print("Training complete. Accuracy:", accuracy_score(y_test, y_pred))

    def identify(self, img_path):
        # Load and process the image
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        features = self.extract_features(image)
        # Predict the category of the image
        category = self.model.predict([features])[0]
        if category == 'close to tree':
            speak("Land the drone, tree is close")
        elif category == 'tree but not closer':
            speak("Approaching a tree")
        else:
            pass
        return category

    def save_model(self, model_path):
        joblib.dump(self.model, model_path)

# Example usage
classifier = ImageClassifier(os.path.join(img_checkpoint_dir, 'tree_classifier.pkl'))
category = classifier.identify(os.path.join(image_proc_dir, 'frame-1715582384.jpg'))

# classifier.load_data()
# classifier.train()
# classifier.save_model(os.path.join(img_checkpoint_dir, 'tree_classifier.pkl'))

