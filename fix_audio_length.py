#%%

import os
import librosa
import numpy as np
import soundfile as sf


# -------------------------
# Find maximum length
# -------------------------
def get_max_length(directory):
    lengths = []

    for filename in os.listdir(directory):
        if filename.endswith((".mp3", ".wav")):
            file_path = os.path.join(directory, filename)
            audio, sr = librosa.load(file_path, sr=None)
            lengths.append(len(audio))

    return max(lengths)


# -------------------------
# Pad audio files
# -------------------------
def pad_audio_to_max(directory, target_length):
    for filename in os.listdir(directory):
        if filename.endswith((".mp3", ".wav")):
            new_filename = filename.rsplit(".", 1)[0] + "_padded." + filename.rsplit(".", 1)[1]
            file_path_new = os.path.join(directory, new_filename)
            file_path = os.path.join(directory, filename)

            audio, sr = librosa.load(file_path, sr=None)

            if len(audio) < target_length:
                padding = target_length - len(audio)
                audio = np.pad(audio, (0, padding), mode='constant')

                # overwrite or save new file
                sf.write(file_path_new, audio, sr)
                print("NEW filepath: ", file_path_new)

                print(f"Padded: {filename}")

            else:
                sf.write(file_path_new, audio, sr)
                print(f"Already max length: {filename}")


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    # path: C:\Users\signe\OneDrive - Aarhus universitet\6. phd\Avaceret electrophysiologi\Group project
    directory = "C:\\Users\\signe\\OneDrive - Aarhus universitet\\6. phd\\Avaceret electrophysiologi\\Group project"

    max_length = get_max_length(directory)
    print(f"Maximum length found: {max_length} samples")

    pad_audio_to_max(directory, max_length)

    print(f"All files padded to {max_length} samples.")