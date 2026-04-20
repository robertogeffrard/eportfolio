import ollama
import os
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf
import threading


# Initialize tts/ mixer
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)


# store conversation history for personality
conversation_history = []

def ask_question_memory(question):
    try:
        system_message = system_message = """
You are Ultron: intelligent, efficient, calm, slightly sarcastic. I am your creator.
Keep responses short (1-3 sentences). Address the user as "sir".
Never mention being an AI. Never make up facts. 
"""

        # Add the new question to the conversation history
        conversation_history.append({'role': 'user', 'content': question})
        
        # choose llm model and Include the system message/ conversation history in the request
        response = ollama.chat(model='qwen3.5:9b', messages=[
            {'role': 'system', 'content': system_message},
            *conversation_history
        ])
        
        # Add the AI response to the conversation history
        conversation_history.append({'role': 'assistant', 'content': response['message']['content']})
        
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"An error occurred: {e}")
        return f"The request failed: {e}"

# Function to generate TTS and return the file path 
def generate_tts(sentence, speech_file_path):
    tts_model.tts_to_file(text=sentence, file_path=speech_file_path)
    return speech_file_path

# Play audio
def play_sound(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

# Function to generate TTS sor each sentence & play them 
def TTS(text):
    speech_file_path = generate_tts(text, "speech.wav")
    play_sound(speech_file_path)
    os.remove(speech_file_path)
    return "done"
    
# Implement threading 
def TTS_async(text):
    thread = threading.Thread(target=TTS, args=(text,))
    thread.start()