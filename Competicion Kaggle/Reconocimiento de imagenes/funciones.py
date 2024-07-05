import pandas as pd
import numpy as np
from PIL import Image
import seaborn as sns
import os
import matplotlib.pyplot as plt

# filter warnings
import warnings
warnings.filterwarnings('ignore')

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.regularizers import l2




def read_csv(file_path):
    return pd.read_csv(file_path)

def load_images_from_csv(csv_path, base_path):
    data = read_csv(csv_path)
    images = []
    labels = []
    
    for _, row in data.iterrows():
        img_path = row[1][1:]
        label = row[2]
        
        # Abrir la imagen
        with Image.open(img_path) as img:
            img = img.convert('L')  # Asegurarse de que esté en escala de grises
            images.append(np.array(img))
            labels.append(label)
    
    return images, labels

def normalize_images(images):
    return [img / 255.0 for img in images]

from sklearn.preprocessing import LabelEncoder

# Definir las emociones
emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
label_encoder = LabelEncoder()
label_encoder.fit(emotions)

def encode_labels(labels):
    return label_encoder.transform(labels)

from tensorflow.keras.utils import to_categorical

def preprocess_labels(labels):
    numeric_labels = encode_labels(labels)
    return to_categorical(numeric_labels, num_classes=len(emotions))


def preprocess_data(images, labels):
    images = np.array(images, dtype=np.float32)
    labels = preprocess_labels(labels)
    
    # Normalizar las imágenes
    images = normalize_images(images)
    
    return images, labels

def count_emotions(csv_path):
    data = read_csv(csv_path)
    emotion_counts = data.iloc[:, 2].value_counts()
    return emotion_counts
