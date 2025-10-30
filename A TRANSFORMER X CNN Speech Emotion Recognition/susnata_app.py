import streamlit as st
import numpy as np
import librosa
import tensorflow as tf
import joblib
import librosa.display
import matplotlib.pyplot as plt

#  Page Config
st.set_page_config(page_title="Susnata's Emotion Recognition", page_icon="🎧", layout="centered")

#  Mint Green Theme
st.markdown("""
    <style>
        body {
            background-color: #d4f7d4;
            color: #033d29;
        }
        .stApp {
            background-color: #d4f7d4;
        }
        h1, h2, h3, h4 {
            color: #054c35;
            text-align: center;
        }
        .stButton>button {
            background-color: #1db954;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #128f46;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎧 Susnata's Emotion Recognition")
st.subheader("CNN + Transformer Model on RAVDESS Dataset")

# 💡 Defining  my custom layers again (Keras needs them when loading)
class PositionalEmbedding(tf.keras.layers.Layer):
    def __init__(self, max_len, d_model, **kwargs):  #  **kwargs added incase some extra attributes
        super(PositionalEmbedding, self).__init__(**kwargs)
        self.pos_emb = tf.keras.layers.Embedding(input_dim=max_len, output_dim=d_model)

    def call(self, x):
        positions = tf.range(start=0, limit=tf.shape(x)[1], delta=1)
        positions = self.pos_emb(positions)
        return x + positions


class TransformerBlock(tf.keras.layers.Layer):
    def __init__(self, embed_dim=32, num_heads=2, ff_dim=64, rate=0.2, **kwargs):
        super().__init__(**kwargs)
        self.att = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim // num_heads)
        self.ffn = tf.keras.Sequential([
            tf.keras.layers.Dense(ff_dim, activation='relu'),
            tf.keras.layers.Dense(embed_dim),
        ])
        self.layernorm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = tf.keras.layers.Dropout(rate)
        self.dropout2 = tf.keras.layers.Dropout(rate)

    def call(self, inputs, training=False):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
#  model loader
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model(
        "susnata_cnn_transformer_emotion2.h5",
        custom_objects={
            "PositionalEmbedding": PositionalEmbedding,
            "TransformerBlock": TransformerBlock
        },
        compile=False
    )
    le = joblib.load("label_encoder2.pkl")
    return model, le

#  Loading once
model, le = load_model()
st.success(" Model loaded successfully!")

#  Feature extraction function same as notebook
def extract_features(file_path, max_pad_len=200):
    audio, sr = librosa.load(file_path, res_type='kaiser_fast')
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    mfcc = (mfcc - np.mean(mfcc, axis=1, keepdims=True)) / (np.std(mfcc, axis=1, keepdims=True) + 1e-6)
    if mfcc.shape[1] < max_pad_len:
        mfcc = np.pad(mfcc, ((0, 0), (0, max_pad_len - mfcc.shape[1])), mode='constant')
    else:
        mfcc = mfcc[:, :max_pad_len]
    return mfcc[..., np.newaxis]

#  File upload section
uploaded_file = st.file_uploader("Upload a .wav file 🎵", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    # Extracting  MFCCs
    features = extract_features(uploaded_file)
    features = np.expand_dims(features, axis=0)

    # Predicting
    preds = model.predict(features)
    predicted_emotion = le.inverse_transform([np.argmax(preds)])[0] #taking argmax
    #Converting that index back to original label like happy calm etc



    st.success(f"🎭 Predicted Emotion: **{predicted_emotion.upper()}**")

    # Display probabilities as bar chart
    fig, ax = plt.subplots()
    emotions = le.classes_
    ax.bar(emotions, preds[0], color='#33cc99')
    ax.set_ylabel("Probability")
    ax.set_title("Emotion Probabilities")
    st.pyplot(fig)

else:
    st.info("Please upload a `.wav` file to detect the emotion.")

st.caption("Model: CNN + Transformer Encoder | Built with ❤ by Susnata ")