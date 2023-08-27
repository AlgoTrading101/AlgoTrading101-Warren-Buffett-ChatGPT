"""Gradio demo for the speaker diarization model."""

import logging

import gradio as gr
import pandas as pd
import psutil

from helpers import whisper_models
from transcription import speech_to_text
from youtube import get_youtube_video


def show_gradio() -> None:
    """Show the Gradio interface."""
    video_in = gr.Video(label="Video file", mirror_webcam=False)
    youtube_url_in = gr.Textbox(label="Youtube url", lines=1, interactive=True)
    df_init = pd.DataFrame(columns=["Start", "End", "Speaker", "Text"])
    memory = psutil.virtual_memory()
    selected_whisper_model = gr.Dropdown(
        choices=whisper_models,
        type="value",
        value="base",
        label="Selected Whisper model",
        interactive=True,
    )
    number_speakers = gr.Number(
        precision=0,
        value=0,
        label="""
        Input the number of speakers for better results.
        If value=0, the model will automatically find the best number of speakers.
        """,
        interactive=True,
    )
    system_info = gr.Markdown(
        f"*Memory: {memory.total / (1024 * 1024 * 1024):.2f}GB,"
        f"used: {memory.percent}%,"
        f"available: {memory.available / (1024 * 1024 * 1024):.2f}GB*"
    )
    download_transcript = gr.File(label="Download transcript")
    transcription_df = gr.DataFrame(
        value=df_init,
        label="Transcription dataframe",
        row_count=(0, "dynamic"),
        max_rows=10,
        wrap=True,
        overflow_row_behaviour="paginate",
    )
    title = "Whisper speaker diarization"
    demo = gr.Blocks(title=title)
    demo.encrypt = False

    with demo:
        gr.Markdown(
            """
                <div>
                <h1 style='text-align: center'>Whisper speaker diarization</h1>
                </div>
                <br>
                This project uses Stable Whisper models for an overall improvement in
                transcription accuracy. \n\n\n

                Whisper: https://github.com/openai/whisper \n
                StableWhisper: https://github.com/jianfch/stable-ts \n
            """
        )

        with gr.Row():
            gr.Markdown(
                """
                    <div>
                    <h2 style='text-align: center'>YouTube Download</h2>
                    </div>
                    """
            )

        with gr.Row():
            gr.Markdown(
                """
                    ### You can test the following examples:
                    """
            )
        gr.Examples(
            examples=[
                "https://youtu.be/bHB8NLY-870",
                "https://www.youtube.com/watch?v=DnpNuRzhxn0",
                "https://youtu.be/ppFlVouq-Mc",
            ],
            label="Examples",
            inputs=[youtube_url_in],
        )

        with gr.Row():
            with gr.Column():
                youtube_url_in.render()
                download_youtube_btn = gr.Button("Download a YouTube video.")
                download_youtube_btn.click(
                    get_youtube_video, [youtube_url_in], [video_in]
                )
                logging.info("Video downloaded.")
                print(video_in)

        with gr.Row():
            with gr.Column():
                video_in.render()

                with gr.Column():
                    gr.Markdown(
                        """
                            <div>
                            <h2 style='text-align: center'>
                                Transcription and Diarization process
                            </h2>
                            </div>
                            """
                    )
                selected_whisper_model.render()
                number_speakers.render()
                transcribe_btn = gr.Button("Start audio transcription and diarization.")

                transcribe_btn.click(
                    speech_to_text,
                    [
                        video_in,
                        selected_whisper_model,
                        number_speakers,
                    ],
                    [transcription_df, system_info, download_transcript],
                )

        with gr.Row():
            gr.Markdown(
                """
                    <div>
                    <h2 style='text-align: center'>Results</h2>
                    </div>
                    """
            )

        with gr.Row():
            with gr.Column():
                download_transcript.render()
                transcription_df.render()
                system_info.render()

    demo.launch(debug=True)
