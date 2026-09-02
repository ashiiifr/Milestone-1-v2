# Milestone 1 – Audio Processing & Transcription

## Task 1 – Whisper Transcription

Test the complete transcription workflow.

**Flow:**
- Upload Meeting Recording
- Process Audio
- Run Whisper
- Generate Transcript
- Display Transcript

---

## Task 2 – File Upload Validation

Verify:
- Audio/video upload works
- Multiple formats supported
- Invalid files are rejected
- Proper error messages are shown

---

## Task 3 – Transcript Validation

Transcript is generated correctly:
- Transcript is not empty
- Transcript matches the recording
- Transcript is saved correctly

---

## Task 4 – Streamlit Interface

Verify:
- File upload
- Transcribe button
- Processing status
- Transcript display

---

## Task 5 – Accuracy Testing

Test multiple recordings:
- Compare transcript with actual speech
- Check missing/incorrect words
- Achieve ≥90% transcription accuracy

---

---

# Milestone 1 – Text Ingestion & Baseline Sentiment

## Task 1 – Validate Text Ingestion Workflow

Test the complete text input process.

**Flow:**
- Create/enter text input
- Upload `.txt` file
- Upload `.csv` file
- Read input data
- Validate input format
- Pass valid text to preprocessing
- Handle empty or invalid inputs
- Verify that all supported input methods work correctly

---

## Task 2 – Preprocessing Validation

Verify that the text preprocessing pipeline works correctly.

**Check:**
- Tokenization
- Stop-word removal
- Lemmatization
- Noise filtering
- Special characters
- Punctuation
- Empty text
- Repeated spaces
- Different text lengths

---

## Task 3 – VADER Sentiment Validation

Verify the baseline sentiment analysis module.

**Check:**
- Positive sentiment detection
- Negative sentiment detection
- Neutral sentiment detection
- Sentiment compound score
- Positive score
- Negative score
- Neutral score
- Test VADER using different sample inputs

---

## Task 4 – Initial Emotion/Sentiment Report Validation

Generate the initial classification report using the sample text corpus.

---

## Task 5 – Complete Pipeline Integration Testing

- Create a GitHub repo: project name
- Get the MIT License
- Push the Milestone 1 code to that repo
- Public repository (not private)
