"""
generate_demo_audio.py
----------------------
Generates demo MP3 audio files of varying durations (≈10s to ≈5min)
using Google Text-to-Speech (gTTS).  Files are saved to ./demo_audio/

Durations are controlled by the length of the spoken text.
English speech averages ~130 words/minute, so:
  ~22 words  ≈  10 seconds
  ~65 words  ≈  30 seconds
  ~130 words ≈  60 seconds (1 min)
  ~325 words ≈  2.5 min
  ~650 words ≈  5 min
"""

import os
from gtts import gTTS

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "demo_audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Demo scripts – each entry is (filename_stem, text)
# ---------------------------------------------------------------------------
DEMOS = [
    # ── ~10 seconds (~22 words) ─────────────────────────────────────────────
    (
        "demo_10s",
        "Welcome to the meeting transcription demo. "
        "This short audio clip lasts approximately ten seconds. "
        "Thank you for listening.",
    ),

    # ── ~30 seconds (~65 words) ─────────────────────────────────────────────
    (
        "demo_30s",
        "Good morning, everyone. Today we are testing the Whisper transcription system "
        "as part of Milestone One. This audio file lasts approximately thirty seconds. "
        "The goal is to verify that short recordings are handled correctly, "
        "that the transcript is not empty, and that the output matches the spoken content. "
        "Thank you.",
    ),

    # ── ~1 minute (~130 words) ──────────────────────────────────────────────
    (
        "demo_1m",
        "Welcome to the one-minute demo recording. "
        "In this test we cover a typical short meeting introduction. "
        "My name is Alex, and I am the project lead for the audio transcription initiative. "
        "Today's agenda includes three items: first, a review of last week's progress; "
        "second, a discussion of the current milestone requirements; "
        "and third, a brief look at the road ahead for the next sprint. "
        "Last week the team completed the audio upload module and integrated it with the "
        "Whisper model backend. Initial accuracy results look promising, sitting above "
        "ninety percent on our test recordings. "
        "This week we move on to validation and edge case testing. "
        "Thank you, and let's get started.",
    ),

    # ── ~2 minutes (~260 words) ─────────────────────────────────────────────
    (
        "demo_2m",
        "Good afternoon. This is the two-minute demo audio clip for the transcription pipeline. "
        "We are going to walk through a simulated project update meeting. "
        "First, let's talk about what was accomplished in the previous sprint. "
        "The team successfully deployed the file upload component, which supports MP3, WAV, "
        "M4A, MP4, OGG, FLAC, and WebM formats. "
        "Invalid file types are now properly rejected with clear error messages. "
        "The Whisper base model has been integrated and is producing transcripts within "
        "a reasonable processing time on standard hardware. "
        "Moving on to current work: the Streamlit interface is now functional. "
        "Users can upload a recording, click the Transcribe button, monitor progress, "
        "and view the full transcript along with timestamped segments. "
        "A download button allows saving the transcript as a plain text file. "
        "We have also added a model selector in the sidebar, so users can choose between "
        "the tiny, base, small, medium, and large Whisper models depending on their "
        "accuracy and speed requirements. "
        "Next steps include running accuracy benchmarks against a set of reference recordings, "
        "targeting ninety percent word accuracy or higher. "
        "We will also add support for speaker diarization in a future milestone. "
        "Thank you for listening to this update. "
        "Please feel free to ask any questions at the end of the session.",
    ),

    # ── ~5 minutes (~650 words) ─────────────────────────────────────────────
    (
        "demo_5m",
        "Hello and welcome to the five-minute demo recording. "
        "This file is designed to test the full transcription pipeline under a longer "
        "audio input, simulating a real meeting scenario. "

        "Let's begin with a project overview. "
        "The goal of Milestone One is to build a robust audio transcription system using "
        "the OpenAI Whisper model, exposed through a Streamlit web interface. "
        "The system accepts audio and video uploads in multiple formats, processes the audio, "
        "runs it through Whisper, and returns a full text transcript to the user. "

        "Now let me describe the technical architecture in more detail. "
        "The application is split into three main modules. "
        "The first module, audio processor, handles file validation and temporary storage. "
        "It checks that the uploaded file has a supported extension and does not exceed "
        "the five-hundred megabyte size limit. "
        "If validation fails, a descriptive error message is shown to the user. "

        "The second module is the transcriber, which wraps the Whisper library. "
        "It loads the selected model, calls the transcribe function with the audio file path, "
        "and returns a structured dictionary containing the full transcript text, "
        "the list of timed segments, the detected language, the model name, and the file name. "
        "The model runs with float32 precision to ensure compatibility on machines "
        "without a CUDA-enabled GPU. "

        "The third module is the Streamlit application itself. "
        "It renders a clean, step-by-step interface that guides the user through "
        "uploading a file, reviewing basic metadata, clicking the transcribe button, "
        "and finally viewing or downloading the output. "
        "The sidebar provides model selection and supported format information. "

        "Let's talk about testing. "
        "We are generating a set of demo audio files at different durations: "
        "ten seconds, thirty seconds, one minute, two minutes, and five minutes. "
        "These files will be used to validate that the transcription pipeline works "
        "correctly across a range of input lengths. "
        "We will measure word error rate by comparing the transcript output against "
        "the known ground truth text of each demo file. "
        "Our target is a word error rate below ten percent, which corresponds to "
        "ninety percent or higher transcription accuracy. "

        "From a user experience perspective, we have paid attention to providing clear "
        "feedback at every stage. "
        "During transcription, a status indicator shows the user that processing is underway. "
        "Once complete, the elapsed time is displayed so users know how long the model took. "
        "Timed segments are shown in an expandable panel for users who want to see "
        "word-level timestamps. "

        "Looking ahead at Milestone Two, we plan to add sentiment analysis using the "
        "VADER library as a baseline, followed by a fine-tuned transformer model "
        "for more nuanced emotion detection. "
        "We will also integrate speaker diarization using the PyAnnote library, "
        "which will allow us to attribute transcript segments to individual speakers. "

        "In terms of infrastructure, the application is designed to run locally in a "
        "Python virtual environment. "
        "A requirements file lists all dependencies, and the virtual environment is "
        "already set up and functional. "
        "Future deployment options include packaging the app as a Docker container "
        "or hosting it on a cloud platform such as Streamlit Community Cloud. "

        "To summarize: Milestone One covers audio upload, validation, transcription, "
        "and transcript display. "
        "The system is working end to end, and we are now focused on accuracy testing "
        "and edge case handling. "
        "This five-minute demo recording represents the longest test case in our suite "
        "and will help us confirm that the pipeline handles extended audio without issues. "

        "Thank you for your attention. "
        "This concludes the five-minute demo recording.",
    ),
]


def generate():
    print(f"Saving demo audio files to: {OUTPUT_DIR}\n")
    for stem, text in DEMOS:
        out_path = os.path.join(OUTPUT_DIR, f"{stem}.mp3")
        print(f"  Generating {stem}.mp3 ...", end=" ", flush=True)
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(out_path)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"saved ({size_kb:.1f} KB)")
    print("\nDone. All demo files generated.")


if __name__ == "__main__":
    generate()
