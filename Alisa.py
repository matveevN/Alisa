from vosk import Model, KaldiRecognizer
import os
import pyaudio
from numba import njit
import threading
import concurrent.futures

# Загрузка модели и инициализация распознавателя
model = Model(r"/home/nikita/Downloads/vosk-model-small-ru-0.22")
rec = KaldiRecognizer(model, 16000)

# Метод для обработки команд с использованием Numba
@njit
def handle_command_numba(command, colors):
    if "алиса" in command:
        for color in colors:
            if color in command:
                if "покажи" in command:
                    print(f"Показываю {color}")
                else:
                    print(f"{color} в командной строке")
                break

# Функция обработки команд с использованием потоков
def process_command(command):
    colors = ["красный", "синий", "зелёный", "жёлтый"]
    handle_command_numba(command, colors)

# Запуск распознавания речи
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16000)

print("Говорите...")

def speech_recognition():
    while True:
        data = stream.read(8000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
           # print(f"Распознанный текст: {result}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(process_command(result))
        

# Создание потока для распознавания речи
speech_thread = threading.Thread(target=speech_recognition)
speech_thread.start()

speech_thread.join() # Ждем завершения потока с распознаванием речи

stream.stop_stream()
stream.close()
p.terminate()
