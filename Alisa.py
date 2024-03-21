from vosk import Model, KaldiRecognizer
from numba import njit
import os
import pyaudio


# Загрузка модели и инициализация распознавателя
model = Model(r"/home/nikita/Downloads/vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, 16000)

# Метод для обработки команд
@njit
def handle_command(command):

    colors = ["красный", "синий", "зелёный", "жёлтый"] # Добавьте другие цвета при необходимости
    if "алиса" in command:
        for color in colors:
            if color in command:
                if "покажи" in command:
                    print(f"Показываю {color}")
                else:
                    print(f"{color} в командной строке")
                break

# Запуск распознавания речи
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

print("Говорите...")
while True:
    data = stream.read(4000)
    if len(data) == 0:
        break        
    if rec.AcceptWaveform(data):
        result = rec.Result()
        handle_command(result)
       # print(f"Распознанный текст: {result}")


stream.stop_stream()
stream.close()
p.terminate()
