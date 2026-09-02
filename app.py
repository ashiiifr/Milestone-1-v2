"""
app.py
------
Streamlit app for Milestone 1 – Task 1: Whisper Transcription
Flow: Upload Meeting Recording → Process Audio → Run Whisper → Generate Transcript → Display Transcript
"""

import streamlit as st
import time
from audio_processor import validate_audio_file, save_uploaded_file, cleanup_temp_file
from transcriber import transcribe_audio, save_transcript, WHISPER_MODELS

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meeting Transcriber",
    page_icon="🎙️",
    layout="centered",
)

st.title("🎙️ Meeting Transcriber")
st.caption("Powered by OpenAI Whisper — Milestone 1 · Task 1")

# ── Sidebar: model selection ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    model_size = st.selectbox(
        "Whisper Model",
        options=WHISPER_MODELS,
        index=1,  # default: 'base'
        help="Larger models are more accurate but slower.",
    )
    st.markdown("---")
    st.markdown(
        "**Supported formats:** mp3, wav, m4a, mp4, ogg, flac, webm  \n"
        "**Max file size:** 500 MB"
    )

# ── Step 1: Upload ────────────────────────────────────────────────────────────
st.subheader("Step 1 · Upload Meeting Recording")
uploaded_file = st.file_uploader(
    "Choose an audio or video file",
    type=["mp3", "wav", "m4a", "mp4", "ogg", "flac", "webm"],
    help="Upload your meeting recording to transcribe.",
)

tmp_path = None  # will hold the temp file path during processing

if uploaded_file is not None:
    # ── Step 2: Process / validate audio ─────────────────────────────────────
    st.subheader("Step 2 · Process Audio")
    is_valid, validation_msg = validate_audio_file(uploaded_file)

    if not is_valid:
        st.error(f"❌ {validation_msg}")
        st.stop()

    st.success(f"✅ {validation_msg}")

    # Show basic file info
    col1, col2 = st.columns(2)
    col1.metric("File Name", uploaded_file.name)
    col2.metric("Size", f"{uploaded_file.size / (1024 * 1024):.2f} MB")

    # ── Step 3: Transcribe ────────────────────────────────────────────────────
    st.subheader("Step 3 · Run Whisper")
    transcribe_btn = st.button("🚀 Transcribe", use_container_width=True, type="primary")

    if transcribe_btn:
        try:
            # Save uploaded bytes to a temp file
            uploaded_file.seek(0)
            tmp_path = save_uploaded_file(uploaded_file)

            # Progress feedback
            status = st.status("Processing…", expanded=True)
            with status:
                st.write("📂 Audio file saved.")
                time.sleep(0.3)

                st.write(f"🤖 Loading Whisper **{model_size}** model…")
                start_time = time.time()

                # ── Step 3 core: run Whisper ──────────────────────────────────
                result = transcribe_audio(tmp_path, model_size=model_size)

                elapsed = time.time() - start_time
                st.write(f"✅ Transcription complete in **{elapsed:.1f}s**.")
                status.update(label="Transcription complete!", state="complete")

            # Persist result in session state so it survives re-runs
            st.session_state["transcript"] = result

        except Exception as exc:
            st.error(f"❌ Transcription failed: {exc}")
        finally:
            cleanup_temp_file(tmp_path)

# ── Step 4 & 5: Generate & Display Transcript ─────────────────────────────────
if "transcript" in st.session_state:
    result = st.session_state["transcript"]

    st.subheader("Step 4 · Transcript")

    # Metadata row
    meta_col1, meta_col2, meta_col3 = st.columns(3)
    meta_col1.metric("Language", result["language"].upper())
    meta_col2.metric("Model", result["model"])
    meta_col3.metric("Segments", len(result["segments"]))

    # Full transcript
    st.markdown("#### Full Transcript")
    if result["text"]:
        st.text_area(
            label="Transcript",
            value=result["text"],
            height=300,
            label_visibility="collapsed",
        )
    else:
        st.warning("⚠️ Transcript is empty — the audio may contain no speech.")

    # Timed segments (optional expandable view)
    if result["segments"]:
        with st.expander("🕐 View timed segments"):
            for seg in result["segments"]:
                start = seg.get("start", 0)
                end = seg.get("end", 0)
                text = seg.get("text", "").strip()
                st.markdown(
                    f"`[{start:6.1f}s → {end:6.1f}s]`  {text}"
                )

    # ── Step 5: Save transcript ───────────────────────────────────────────────
    st.subheader("Step 5 · Save Transcript")

    col_save, col_download = st.columns(2)

    with col_save:
        save_path = st.text_input(
            "Save path (.txt)",
            value=f"transcript_{result['file']}.txt",
        )
        if st.button("💾 Save to file"):
            try:
                saved = save_transcript(result["text"], save_path)
                st.success(f"Saved to `{saved}`")
            except Exception as exc:
                st.error(f"Failed to save: {exc}")

    with col_download:
        st.download_button(
            label="⬇️ Download transcript",
            data=result["text"],
            file_name=f"transcript_{result['file']}.txt",
            mime="text/plain",
            use_container_width=True,
        )
