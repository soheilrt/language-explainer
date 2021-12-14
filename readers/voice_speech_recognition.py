from speech_recognition import AudioData, Recognizer

from models.reader import Reader
import speech_recognition as sr


class VoiceRecognition(Reader):
    def __init__(self, file_name: str):
        super().__init__()
        self.__file_name: str = file_name
        self.__r: Recognizer = sr.Recognizer()

    def read(self) -> str:
        with sr.AudioFile(open(self.__file_name,'rb')) as audio_file:
            print("reading audio file...")
            audio_data = self.__r.record(audio_file)
            print("extracting text from audio file...")
            return self.__recognize(audio_data)

    def __recognize(self, audio_data: AudioData) -> str:
        return self.__r.recognize_google(audio_data)
