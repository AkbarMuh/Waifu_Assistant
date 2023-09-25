import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import streamlit as st
from gpt4free import you
import openai
from gtts import gTTS
import random

def get_answer(question: str) -> str:
    # Set cloudflare clearance cookie and get answer from GPT-4 model
    try:
        openai.api_key = open("key.txt", "r").read().strip("\n")
        messages = [ {"role": "system", "content": 
                    "Namamu adalah Nahida, perkenalkan dirimu sebelum menjawab pertanyaan. Jawab pertanyaan berikut dengan baik."} ]
        #while True:
        #message = input("User : ")
        message = question  
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        # Return error message if an exception occurs
        return (
            f'An error occurred: {e}. Please make sure you are using a valid cloudflare clearance token and user agent.'
        )


# Set page configuration and add header
st.set_page_config(
    page_title="Waifu Generatif",
    initial_sidebar_state="expanded",
    page_icon="🧠",
    menu_items={
        'Get Help': 'https://github.com/xtekky/gpt4free/blob/main/README.md',
        'Report a bug': "https://github.com/xtekky/gpt4free/issues",
        'About': "### gptfree GUI",
    },
)
st.header('Waifu Generator')


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""	

def VoiceGTTS(hasilgpt):
    kodeSuara = str(random.randint(10000000000,1000000000000000000))
    speak = gTTS(text="" + hasilgpt, lang="id", slow=False)
    audio_path = "./Voice_AI/captured_voice"+kodeSuara+".mp3"
    speak.save(audio_path)
    st.audio(audio_path)

def Natural_Voice(hasilgpt):
    from elevenlabs import clone, generate, play, set_api_key, save
    from elevenlabs.api import History
    set_api_key("6b5b2cfbb952aff99001c460c4355b5c")

    kodeSuara = str(random.randint(10000000000,1000000000000000000))

    # speak = generate(
    # #text=hasilgpt[:200],
    # text=hasilgpt,
    # voice="Rani",
    # model="eleven_multilingual_v2"
    # )
    # voice = clone(
    # name="Nahida",
    # description="Dendro archon",
    # files=["./Sample/Nahida(1).mp3", "./Sample/Nahida(2).mp3", "./Sample/Nahida(3).mp3", "./Sample/Nahida(4).mp3", "./Sample/Nahida(5).mp3", "./Sample/Nahida(6).mp3", "./Sample/Nahida(7).mp3", "./Sample/Nahida(8).mp3", "./Sample/Nahida(9).mp3", "./Sample/Nahida(10).mp3"],
    # )
    
    speak = generate(text=hasilgpt, voice="Nahida",model="eleven_multilingual_v2")
    
    play(speak)

    audio_path = "./Voice_AI/captured_voice"+kodeSuara+".mp3"
    save(speak, audio_path)
    st.audio(audio_path)

from streamlit_login_auth_ui.widgets import __login__

__login__obj = __login__(auth_token = "courier_auth_token", 
                    company_name = "Shims",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN:

    st.markdown("Selamat Sudah Login")
    question_text_area = st.text_area('🤖 Tanya :', placeholder='Ini tempat buat pertanyaan')
    eleven = st.checkbox("Natural Voice ?")

    from audiorecorder import audiorecorder
    import speech_recognition as sr

    c=st.container()
    with c:
        audio = audiorecorder("Start","Recognizer ...")
    
    if len(audio) > 0:
        wav_file = open("input.mp3", "wb")
        wav_file.write(audio.tobytes())

        import time
        t = time.localtime()
        waktu = time.strftime("%H_%M_%S", t)
        current_time = waktu 
        filesuara = "./suara/"+current_time+".wav"
        import subprocess
        subprocess.call(['ffmpeg', '-i', 'input.mp3',
                        filesuara]) 
        r = sr.Recognizer()
        harvard = sr.AudioFile(filesuara)
        with harvard as source:
            audio = r.record(source)
            output = r.recognize_google(audio, language='id')
            output = output.title()
            st.text(output + " ?")

        
        hasil = get_answer(output)
        st.markdown(hasil)
        if eleven:
            Natural_Voice(hasil)
        else:
            VoiceGTTS(hasil)

    if st.button('🧠 Think'):
        answer = get_answer(question_text_area)
        #escaped = answer
        # Display answer
        st.caption("Answer :")
        st.markdown(answer)
        if eleven:
            Natural_Voice(answer)
        else:
            VoiceGTTS(answer)
    
    
