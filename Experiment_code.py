from psychopy import visual, core, event, sound, prefs
import random
from psychopy.constants import PLAYING, FINISHED
import csv
import os
from datetime import datetime

win = visual.Window(
    size=(800, 600),
    monitor="testMonitor",  # or your calibrated monitor
    units="height",
    color="black"
)

# -------------------------
# AUDIO BACKEND (better timing)
# -------------------------
prefs.hardware['audioLib'] = ['ptb']  # PsychToolbox backend
 
# -------------------------
# PRELOAD SOUNDS (run once!)
# -------------------------
number_sounds = {
    i: sound.Sound(f"{i}.mp3")
    for i in range(0, 9)
}

# -------------------------
# SETUP
# -------------------------
win = visual.Window(size=(800, 600), color="black", units="height")
clock = core.Clock()

text_stim = visual.TextStim(win, text="", height=0.1, color="white")
fixation = visual.TextStim(win, text="+", height=0.1, color="white")


# -------------------------
# ENCODING FUNCTION
# -------------------------
# paradigm_types = ["sequential audio", "regular visual", "sequential visual"]

def create_stimuli(memory_set, paradigm_type):

    # Simultaneous visual
    if paradigm_type == "regular visual":
        memory_string = "   ".join(str(n) for n in memory_set)
        text_stim.text = memory_string
        text_stim.pos = (0, 0)
        text_stim.draw()
        win.flip()
        core.wait(0.2)

    # Sequential visual
    elif paradigm_type == "sequential visual":
        for num in memory_set:
            text_stim.text = str(num)
            text_stim.pos = (0, 0)
            text_stim.draw()
            win.flip()
            core.wait(0.34)

            win.flip()

    # Sequential "audio" (placeholder using visual numbers)
    elif paradigm_type == "sequential audio":
        text_stim.text = "+"
        text_stim.pos = (0, 0)
        text_stim.draw()
        win.flip()  # blank screen once before sequence

        for num in memory_set:
            snd = sound.Sound(f"{num}_padded.mp3")
            snd.play()
            core.wait(snd.getDuration())


# -------------------------
# TRIAL FUNCTION
# -------------------------
def run_trial(trial_type, paradigm_type):
    # Generate memory set
    memory_set = random.sample(range(0, 9), 6)

    if trial_type == "present":
        probe = random.choice(memory_set)
        correct_answer = "y"
    else:
        remaining = list(set(range(0, 9)) - set(memory_set))
        probe = random.choice(remaining)
        correct_answer = "n"

    # -------------------------
    # Encoding
    # -------------------------
    create_stimuli(memory_set, paradigm_type)

    # -------------------------
    # Retention
    # -------------------------
    fixation.draw()
    win.flip()
    core.wait(2.8)

    # -------------------------
    # Probe
    # -------------------------
    text_stim.text = str(probe)
    text_stim.draw()
    win.flip()

    clock.reset()

    keys = event.waitKeys(
        keyList=["y", "n", "escape"],
        timeStamped=clock
    )

    key, rt = keys[0]

    if key == "escape":
        win.close()
        core.quit()

    correct = int(key == correct_answer)

    return {
        "memory_set": memory_set,
        "probe": probe,
        "trial_type": trial_type,
        "paradigm": paradigm_type,
        "response": key,
        "rt": rt,
        "correct": correct
    }


# -------------------------
# EXPERIMENT LOOP
# -------------------------
text_stim.text = "Welcome to the experiment! Press any key to start."
text_stim.draw()
win.flip()
event.waitKeys()


paradigm_types = ["sequential audio", "regular visual", "sequential visual"]

results = []

# 10 trials pr block, 5 rounds 
n_blocks = 1
trials_per_block = 2

for block in range(n_blocks):
    for paradigm_type in paradigm_types:
        # print screen to show what paradigm is starting
        text_stim.text = f"Starting {paradigm_type} block"
        text_stim.draw()
        win.flip()
        core.wait(2)

        # Balanced present/absent
        trial_types = ["present"] * (trials_per_block // 2) + \
                      ["absent"] * (trials_per_block // 2)

        random.shuffle(trial_types)

        for trial_type in trial_types:
            data = run_trial(trial_type, paradigm_type)
            results.append(data)


        # print that paradigm block is ending
        text_stim.text = f"Ending {paradigm_type} block. \nPress any key to continue to next paradigm"
        text_stim.draw()
        win.flip()
        event.waitKeys()
        
# Choose a filename and folder
output_dir = os.getcwd()  # current working directory

# Get current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # e.g., 20260330_153210

# Build output filename
output_file = os.path.join(output_dir, f"experiment_results_{timestamp}.csv")

print(output_file)

# If there are results
if results:
    # Get the fieldnames from the keys of the first trial
    fieldnames = results[0].keys()

    with open(output_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write all trial rows
        for trial in results:
            writer.writerow(trial)

    print(f"Results saved to: {output_file}")
else:
    print("No results to save.")


text_stim.text = "Experiment complete! Thank you!"
text_stim.draw()
win.flip()
core.wait(3)


# -------------------------
# CLEAN UP
# -------------------------
win.close()
core.quit()