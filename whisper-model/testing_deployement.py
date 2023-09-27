import os
import multiprocessing
import numpy as np
import torch
import pandas as pd
import whisper
import torchaudio
import sagemaker
import time
from tqdm.notebook import tqdm

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class LibriSpeech(torch.utils.data.Dataset):
    """
    A simple class to wrap LibriSpeech and trim/pad the audio to 30 seconds.
    It will drop the last few seconds of a very small portion of the utterances.
    """
    def __init__(self, split="test-clean", device=DEVICE):
        self.dataset = torchaudio.datasets.LIBRISPEECH(
            root=os.path.expanduser("~/.cache"),
            url=split,
            download=True,
        )
        self.device = device

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        audio, sample_rate, text, _, _, _ = self.dataset[item]
        assert sample_rate == 16000
        audio = whisper.pad_or_trim(audio.flatten()).to(self.device)
        mel = whisper.log_mel_spectrogram(audio)
        
        return (mel, text)


dataset = LibriSpeech("test-clean")
loader = torch.utils.data.DataLoader(dataset, batch_size=16)
model = whisper.load_model("base.en")
print(
    f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
    f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
)
audio, sample_rate, text, _, _, _ = dataset.dataset[0]


whisper_endpoint = sagemaker.predictor.Predictor('-----------------------')
whisper_endpoint.serializer = sagemaker.serializers.NumpySerializer()

assert whisper_endpoint.endpoint_context().properties['Status'] == 'InService'

inp = audio.cpu().numpy()
out = whisper_endpoint.predict(inp)
print(f'Example Transcription: \n{out}')