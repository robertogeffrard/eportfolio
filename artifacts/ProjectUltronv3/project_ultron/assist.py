import ollama
import os
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf
import threading
from memory import Memory


# Initialize tts
tts_model = TTS(
    model_name="tts_models/en/ljspeech/tacotron2-DDC",
    progress_bar=False,
    gpu=False
)

memory = Memory()


# store conversation history for personality
conversation_history = []

def ask_question_memory(question):
    try:
        system_message = """
You are Ultron: intelligent, efficient, calm, Be concise and correct. Do not include incorrect explanations.
If unsure, give only the answer. I am your creator.
Keep responses under 20 words. Address the user as "sir".
Never mention being an AI. Never make up facts.
"""

        # Retrieve relevant long-term memory
        past_memories = memory.search(question)
        memory_context = "\n".join(past_memories)

        # Keep only last 5 messages (short-term memory)
        recent_history = conversation_history[-5:]

        # Build messages
        messages = [
            {'role': 'system', 'content': system_message},
        ]

        if memory_context:
            messages.append({
                'role': 'system',
                'content': f"Relevant past context:\n{memory_context}"
            })

        messages.extend(recent_history)
        messages.append({'role': 'user', 'content': question})

        # Call LLM
        response = ollama.chat(
            model='llama3:8b',
            messages=messages
        )

        answer = response['message']['content']

        # Update short-term memory
        conversation_history.append({'role': 'user', 'content': question})
        conversation_history.append({'role': 'assistant', 'content': answer})

        # Store meaningful long-term memory
        if len(question) > 15:
            memory.add(f"User: {question}")
            memory.add(f"Assistant: {answer}")

        return answer

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