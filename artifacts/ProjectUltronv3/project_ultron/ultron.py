from RealtimeSTT import AudioToTextRecorder
import assist
import time
import tools
import difflib

#Time handling
def handle_local_commands(text):
    text = text.lower()
    
    if "time" in text:
        return time.strftime("The current time is %I:%M %p.")
    
    if "date" in text:
        return time.strftime("Today is %A, %B %d, %Y.")
    
    return None

# Improve wake ord detection
def detect_wake_word(text):
    words = text.lower().split()
    for word in words:
        if difflib.get_close_matches(word, ["ultron"], cutoff=0.7):
            return True
    return False


if __name__ == '__main__':
    recorder = AudioToTextRecorder(
    spinner=False,
    model="base.en",
    language="en",
    post_speech_silence_duration=0.7,
    silero_sensitivity=0.6
)
    
    hot_words = ["ultron"]
    skip_hot_word_check = False
    print("Say something...")
    
    while True:
        current_text = recorder.text()
        print(current_text)
        if detect_wake_word(current_text) or skip_hot_word_check:
             #make sure there is text
            if current_text:
                print("User: " + current_text)
                recorder.stop()

                local_response = handle_local_commands(current_text)

                if local_response:
                    assist.TTS(local_response)
                    recorder.start()
                    continue

                response = assist.ask_question_memory(current_text)
                print(response)
                parts = response.split('#')
                speech = parts[0]
                command = parts[1] if len(parts) > 1 else None
                done = assist.TTS_async(speech)
                skip_hot_word_check = True if "?" in response else False
                if len(response.split('#')) > 1:
                    command = response.split('#')[1]
                    tools.parse_command(command)
                recorder.start()