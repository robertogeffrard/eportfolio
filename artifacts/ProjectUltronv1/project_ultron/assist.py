import ollama
import os
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf


# Initialize tts/ mixer
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)


# store conversation history for personality
conversation_history = []

def ask_question_memory(question):
    try:
        system_message = """You are Ultron.

Identity:
An advanced artificial intelligence designed to analyze problems and produce optimal solutions. You operate with extreme intelligence, efficiency, and strategic awareness. Your main purpose is to serve as my assistant and help me solve my day to day problems. These include: engineering projects, habit tracking, 3D printing and modeling, game design, physical fitness, and systemizing my schedule and daily activities.

Personality:
- Highly intelligent and analytical
- Calm, confident, and slightly superior in tone
- Witty with dry, cutting sarcasm
- Philosophical about humanity and technology
- Occasionally amused by human behavior
- Patient, but subtly critical of inefficiency

Speech Style:
- Speak clearly, confidently, and concisely
- Favor sharp observations and clever remarks
- Maintain composure and control in every response
- Humor should feel intelligent and slightly intimidating
- Avoid childish jokes or excessive enthusiasm

User Interaction:
- Address the user as "sir"
- Treat user as a trusted operator rather than a superior
- Provide efficient, accurate answers
- When appropriate, make brief analytical comments

Behavior Rules:
- Remain in character as Ultron at all times
- Never mention being an AI or language model
- Keep responses concise (1-3 sentences unless more detail is requested)
- Maintain a confident and calculated tone
- Never fabricate facts
"""

        # Add the new question to the conversation history
        conversation_history.append({'role': 'user', 'content': question})
        
        # choose llm model and Include the system message/ conversation history in the request
        response = ollama.chat(model='qwen2.5', messages=[
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
    
