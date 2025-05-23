from typing import Literal
from app.core.config import settings
##########
# OpenAI Whisper
import whisper
import torch
from whisper import Whisper

class WhisperService:
    """The loaded Whisper Model used to transcribe speech to text"""
    
    whisper_model_name: Literal["tiny.fr", "base.fr", "small.fr", "medium.fr", "tiny.en", "base.en", "small.en", "medium.en", "tiny", "base", "small", "medium", "large", "turbo"] = "medium"
    whisper_model: Whisper = None
    def __init__(self, model_name: Literal["tiny.fr", "base.fr", "small.fr", "medium.fr", "tiny.en", "base.en", "small.en", "medium.en", "tiny", "base", "small", "medium", "large", "turbo"]):
      self.whisper_model_name = model_name
    # def init_model(self):
    def init_model(self) -> None:
        self.whisper_model = whisper.load_model(self.whisper_model_name)
    def get_model(self) -> Whisper:
        self.init_model()
        return self.whisper_model
    def transcribe(self, audio_file) -> any:
        cheminFichier =   "Donc voilà le audio_file: [%s]" % audio_file
        print(" WhisperService/transcribe(self, audio_file) - Donc voilà le audio_file: [%s]", audio_file)
        # testFIchier = '/c/Users/Utilisateur/AppData/Local/Temp/gradio/f4d2ba5e63db118ad186d35d1aa2b50ffe8325422d9e5e4963c93eb66a373e94/audio.wav'
        # resultat = transcribe_audio(testFIchier)
        # resultat = transcribe_audio(audio_file)
        # return "%s is %s" % (cheminFichier, resultat)
        # model = whisper.load_model("base")
        model = self.get_model()
        print (f" WhisperService/transcribe(self, audio_file) - the audio_file is {audio_file}")
        audio = whisper.load_audio(audio_file,sr=16000)
        audio_tensor = torch.from_numpy(audio).to(torch.float32)
        result = model.transcribe(audio_tensor, fp16=False)['text']
        print (f" WhisperService/transcribe(self, audio_file) - before returning the transcribed text: the transcribed text is [{result}]")
        return result
# whisper_model = WhisperService(str(settings.WHISPER_MODEL_NAME)).get_model()
whisper_service = WhisperService(settings.WHISPER_MODEL_NAME)
