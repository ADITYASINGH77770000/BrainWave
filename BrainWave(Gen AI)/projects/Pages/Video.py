import streamlit as st
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim import corpora, models
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.downloader import Downloader

downloader = Downloader()

nltk.download('punkt')
nltk.download('stopwords')
if not downloader.is_installed('punkt_tab'):
  nltk.download('punkt_tab')

stop_words = set(stopwords.words('english'))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 550 words. Please provide the summary of the text given here:  """


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

# Function to vectorize a sentence
def vectorize_sentence(sentence, max_length):
    tokens = word_tokenize(sentence)
    filtered_tokens = [token.lower() for token in tokens if token.isalnum() and token.lower() not in stop_words]
    
    vector = np.zeros(max_length) #This is a fixed size numpy vector
    for i, token in enumerate(filtered_tokens):
      if i< max_length:
        vector[i] = 1
    return vector
    
# Function to calculate sentence similarity using cosine similarity
def calculate_sentence_similarity(sentence1, sentence2, max_length):
    vec1 = vectorize_sentence(sentence1, max_length).reshape(1, -1)
    vec2 = vectorize_sentence(sentence2, max_length).reshape(1, -1)
    
    if np.count_nonzero(vec1) == 0 or np.count_nonzero(vec2) == 0: #handle cases with empty vectors
      return 0
    similarity = cosine_similarity(vec1, vec2)[0][0]
    return similarity


# Function to select most representative sentences
def select_representative_sentences(transcript_text, n_sentences=5):
  sentences = sent_tokenize(transcript_text)
  if len(sentences) <= n_sentences:
    return sentences
  
  all_tokens = [word_tokenize(sent) for sent in sentences]
  filtered_tokens = [ [token.lower() for token in tokens if token.isalnum() and token.lower() not in stop_words] for tokens in all_tokens]
  max_length = max(len(tokens) for tokens in filtered_tokens)

  sentence_vectors = [vectorize_sentence(sent, max_length) for sent in sentences]


  # create a matrix for efficient similarity comparison
  matrix = np.array(sentence_vectors)
    # compute the cosine similarity matrix for all the sentences
  similarity_matrix = cosine_similarity(matrix)
    
    #compute the average score for each sentence in the corpus
  sentence_scores = np.sum(similarity_matrix, axis=1)

  ranked_sentence_indices = np.argsort(sentence_scores)[::-1]

    #extract the top sentences
  top_sentences = [sentences[i] for i in ranked_sentence_indices[:n_sentences]]
  return top_sentences
def resolve_coreferences(text):
    return text

# Function for abstractive summarization using Gemini Pro
def generate_gemini_summary(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to perform topic modeling using gensim
def perform_topic_modeling(transcript_text, num_topics=3):
    # Tokenize and remove stopwords
    tokens = [word.lower() for word in word_tokenize(transcript_text) if word.isalpha() and word.lower() not in stop_words]

    #Create dictionary of tokens
    dictionary = corpora.Dictionary([tokens])
    corpus = [dictionary.doc2bow(tokens)]
    
    # Train LDA
    lda_model = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)
    topics = lda_model.print_topics(num_words=5)

    return topics

# Function to perform named entity recognition (Placeholder)
def perform_ner(transcript_text):
    return []


# Main function for generating summaries
def generate_enhanced_summary(transcript_text):
    # 1. Sentence Selection based on Similarity
    representative_sentences = select_representative_sentences(transcript_text)
    representative_sentences_text = " ".join(representative_sentences)

    #2. Coreference Resolution
    resolved_text = resolve_coreferences(representative_sentences_text)

    #3. Abstractive Summarization
    abstractive_summary = generate_gemini_summary(resolved_text, prompt)

    # 4. Topic Modeling
    topics = perform_topic_modeling(transcript_text)

    #5. Named Entity Recognition
    entities = perform_ner(transcript_text)

    return {
        "representative_sentences": representative_sentences,
        "abstractive_summary": abstractive_summary,
        "topics": topics,
        "entities": entities,
    }
#Main App code

st.set_page_config(page_title="YouTube Video Summarizer", page_icon="📹",layout="wide")

st.title("📹 YouTube Video Summarizer")

# Add a green line before FAQ
st.markdown("<hr style='border: 3px solid green;'>", unsafe_allow_html=True)
# Input Box

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)


if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        enhanced_summary = generate_enhanced_summary(transcript_text)

        st.markdown("## 📝 Detailed Notes:")
        st.markdown("### Abstractive Summary:")
        st.write(enhanced_summary["abstractive_summary"])
        st.markdown("### Representative Sentences:")
        st.write(enhanced_summary["representative_sentences"])
        st.markdown("### Key Topics:")
        st.write(enhanced_summary["topics"])
        st.markdown("### Named Entities:")
        st.write(enhanced_summary["entities"])


# Add a green line before FAQ
st.markdown("<hr style='border: 3px solid green;'>", unsafe_allow_html=True)

# FAQ Section
st.subheader("Frequently Asked Questions (FAQ)")

with st.expander("Q1: What is the purpose of this YouTube Transcript Summarizer tool?"):
    st.write("This tool allows you to input a YouTube video link and get a detailed summary based on the transcript of the video. It leverages advanced AI capabilities to analyze and summarize the content, making it useful for various applications such as content creation, research, and more.")

with st.expander("Q2: How do I use this YouTube Transcript Summarizer tool?"):
    st.write("Simply enter the YouTube video link in the provided input field and click the 'Get Detailed Notes' button. The model will process your input and generate a detailed summary of the video's transcript.")

with st.expander("Q3: What kind of videos can I summarize?"):
    st.write("You can summarize any YouTube video that has a transcript available. The tool works best with videos that have clear and well-structured transcripts.")

with st.expander("Q4: What should I do if the generated summary is not accurate?"):
    st.write("If the generated summary does not meet your expectations, try refining your input prompt with more details or different wording. The model's output can vary based on the input, so experimenting with different prompts can help achieve better results.")

with st.expander("Q5: Can I use the generated summaries for commercial purposes?"):
    st.write("The generated summaries are for demonstration purposes and may be subject to the terms and conditions of the model and the platform. Please review the usage policies and licensing agreements before using the summaries for commercial purposes.")