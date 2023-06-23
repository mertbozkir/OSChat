import base64
from pathlib import Path

from typing import IO
import io

from utils.outputs.text_to_speech import text_to_speech, TextToSpeechConfig
import streamlit as st


def autoplay_audio(audio: str | io.BytesIO):
    if isinstance(audio, str):
        with open(audio, "rb") as f:
            data = f.read()
    elif isinstance(audio, io.BytesIO):
        data = audio.getvalue()
        audio.seek(0)
    else:
        raise ValueError("Invalid audio input type.")

    b64 = base64.b64encode(data).decode()
    md = f"""
        <audio controls autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(
        md,
        unsafe_allow_html=True,
    )


def handle_text_2_speech(text: str | Path | IO):
    if not text:
        st.error(f"invalid input:{type(text)}")
        return

    config = TextToSpeechConfig(text=text, output=io.BytesIO())
    text_to_speech(config)
    # st.audio(config.output, config.format, start_time=0)
    autoplay_audio(config.output)
