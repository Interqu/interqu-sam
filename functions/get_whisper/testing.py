import json
import time
import whisper

full = time.time()
model = whisper.load_model("medium")
start = time.time()
result = model.transcribe("../")
end = time.time()
print(end - start)
print("\n")
print(end - full)
print("\n")

print(result["text"])

