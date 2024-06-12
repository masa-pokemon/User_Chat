
import streamlit as st
user_msg = st.chat_input("Enter your message")
col1, col2,col3 = st.columns(3)
with col1:
    import logging
    import math
    from typing import List

    try:
        from typing import Literal
    except ImportError:
        from typing_extensions import Literal  # type: ignore

    import av
    import cv2
    import numpy as np
    from streamlit_server_state import server_state, server_state_lock

    from streamlit_webrtc import (
        VideoProcessorBase,
        WebRtcMode,
        WebRtcStreamerContext,
        create_mix_track,
        create_process_track,
        webrtc_streamer,
    )

    logger = logging.getLogger(__name__)


    class OpenCVVideoProcessor(VideoProcessorBase):
        type: Literal["noop", "cartoon", "edges", "rotate"]

        def __init__(self) -> None:
            self.type = "noop"

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            if self.type == "noop":
                pass
            elif self.type == "cartoon":
                # prepare color
                img_color = cv2.pyrDown(cv2.pyrDown(img))
                for _ in range(6):
                    img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
                img_color = cv2.pyrUp(cv2.pyrUp(img_color))

                # prepare edges
                img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img_edges = cv2.adaptiveThreshold(
                    cv2.medianBlur(img_edges, 7),
                    255,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY,
                    9,
                    2,
                )
                img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

                # combine color and edges
                img = cv2.bitwise_and(img_color, img_edges)
            elif self.type == "edges":
                # perform edge detection
                img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
            elif self.type == "rotate":
                # rotate image
                rows, cols, _ = img.shape
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
                img = cv2.warpAffine(img, M, (cols, rows))

            return av.VideoFrame.from_ndarray(img, format="bgr24")


    def mixer_callback(frames: List[av.VideoFrame]) -> av.VideoFrame:
        buf_w = 640
        buf_h = 480
        buffer = np.zeros((buf_h, buf_w, 3), dtype=np.uint8)

        n_inputs = len(frames)

        n_cols = math.ceil(math.sqrt(n_inputs))
        n_rows = math.ceil(n_inputs / n_cols)
        grid_w = buf_w // n_cols
        grid_h = buf_h // n_rows

        for i in range(n_inputs):
            frame = frames[i]
            if frame is None:
                continue

            grid_x = (i % n_cols) * grid_w
            grid_y = (i // n_cols) * grid_h

            img = frame.to_ndarray(format="bgr24")
            src_h, src_w = img.shape[0:2]

            aspect_ratio = src_w / src_h

            window_w = min(grid_w, int(grid_h * aspect_ratio))
            window_h = min(grid_h, int(window_w / aspect_ratio))

            window_offset_x = (grid_w - window_w) // 2
            window_offset_y = (grid_h - window_h) // 2

            window_x0 = grid_x + window_offset_x
            window_y0 = grid_y + window_offset_y
            window_x1 = window_x0 + window_w
            window_y1 = window_y0 + window_h

            buffer[window_y0:window_y1, window_x0:window_x1, :] = cv2.resize(
                img, (window_w, window_h)
            )

        new_frame = av.VideoFrame.from_ndarray(buffer, format="bgr24")

        return new_frame


    def main():
        with server_state_lock["webrtc_contexts"]:
            if "webrtc_contexts" not in server_state:
                server_state["webrtc_contexts"] = []

        with server_state_lock["mix_track"]:
            if "mix_track" not in server_state:
                server_state["mix_track"] = create_mix_track(
                    kind="video", mixer_callback=mixer_callback, key="mix"
                )

        mix_track = server_state["mix_track"]

        self_ctx = webrtc_streamer(
            key="self",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": True},
            source_video_track=mix_track,
            sendback_audio=False,
        )

        self_process_track = None
        if self_ctx.input_video_track:
            self_process_track = create_process_track(
                input_track=self_ctx.input_video_track,
                processor_factory=OpenCVVideoProcessor,
            )
            mix_track.add_input_track(self_process_track)

            self_process_track.processor.type = st.radio(
                "Select transform type",
                ("noop", "cartoon", "edges", "rotate"),
                key="filter1-type",
            )

        with server_state_lock["webrtc_contexts"]:
            webrtc_contexts: List[WebRtcStreamerContext] = server_state["webrtc_contexts"]
            self_is_playing = self_ctx.state.playing and self_process_track
            if self_is_playing and self_ctx not in webrtc_contexts:
                webrtc_contexts.append(self_ctx)
                server_state["webrtc_contexts"] = webrtc_contexts
            elif not self_is_playing and self_ctx in webrtc_contexts:
                webrtc_contexts.remove(self_ctx)
                server_state["webrtc_contexts"] = webrtc_contexts

        if self_ctx.state.playing:
            # Audio streams are transferred in SFU manner
            # TODO: Create MCU to mix audio streams
            for ctx in webrtc_contexts:
                if ctx == self_ctx or not ctx.state.playing:
                    continue
                webrtc_streamer(
                    key=f"sound-{id(ctx)}",
                    mode=WebRtcMode.RECVONLY,
                    rtc_configuration={
                        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                    },
                    media_stream_constraints={"video": False, "audio": True},
                    source_audio_track=ctx.input_audio_track,
                    desired_playing_state=ctx.state.playing,
                )


    if __name__ == "__main__":
        import os

        DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]

        logging.basicConfig(
            format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
            "%(message)s",
            force=True,
        )

        logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

        st_webrtc_logger = logging.getLogger("streamlit_webrtc")
        st_webrtc_logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

        aioice_logger = logging.getLogger("aioice")
        aioice_logger.setLevel(logging.WARNING)

        fsevents_logger = logging.getLogger("fsevents")
        fsevents_logger.setLevel(logging.WARNING)

        main()
with col3:
    import logging
    import logging.handlers
    import queue
    import threading
    import time
    import urllib.request
    import os
    from collections import deque
    from pathlib import Path
    from typing import List

    import av
    import numpy as np
    import pydub
    import streamlit as st
    from twilio.rest import Client

    from streamlit_webrtc import WebRtcMode, webrtc_streamer

    HERE = Path(__file__).parent

    logger = logging.getLogger(__name__)


    # This code is based on https://github.com/streamlit/demo-self-driving/blob/230245391f2dda0cb464008195a470751c01770b/streamlit_app.py#L48  # noqa: E501
    def download_file(url, download_to: Path, expected_size=None):
        # Don't download the file twice.
        # (If possible, verify the download using the file length.)
        if download_to.exists():
            if expected_size:
                if download_to.stat().st_size == expected_size:
                    return
            else:
                st.info(f"{url} is already downloaded.")
                if not st.button("Download again?"):
                    return

        download_to.parent.mkdir(parents=True, exist_ok=True)

        # These are handles to two visual elements to animate.
        weights_warning, progress_bar = None, None
        try:
            weights_warning = st.warning("Downloading %s..." % url)
            progress_bar = st.progress(0)
            with open(download_to, "wb") as output_file:
                with urllib.request.urlopen(url) as response:
                    length = int(response.info()["Content-Length"])
                    counter = 0.0
                    MEGABYTES = 2.0 ** 20.0
                    while True:
                        data = response.read(8192)
                        if not data:
                            break
                        counter += len(data)
                        output_file.write(data)

                        # We perform animation by overwriting the elements.
                        weights_warning.warning(
                            "Downloading %s... (%6.2f/%6.2f MB)"
                            % (url, counter / MEGABYTES, length / MEGABYTES)
                        )
                        progress_bar.progress(min(counter / length, 1.0))
        # Finally, we remove these visual elements by calling .empty().
        finally:
            if weights_warning is not None:
                weights_warning.empty()
            if progress_bar is not None:
                progress_bar.empty()


    # This code is based on https://github.com/whitphx/streamlit-webrtc/blob/c1fe3c783c9e8042ce0c95d789e833233fd82e74/sample_utils/turn.py
    @st.cache_data  # type: ignore
    def get_ice_servers():
        """Use Twilio's TURN server because Streamlit Community Cloud has changed
        its infrastructure and WebRTC connection cannot be established without TURN server now.  # noqa: E501
        We considered Open Relay Project (https://www.metered.ca/tools/openrelay/) too,
        but it is not stable and hardly works as some people reported like https://github.com/aiortc/aiortc/issues/832#issuecomment-1482420656  # noqa: E501
        See https://github.com/whitphx/streamlit-webrtc/issues/1213
        """

        # Ref: https://www.twilio.com/docs/stun-turn/api
        try:
            account_sid = os.environ["TWILIO_ACCOUNT_SID"]
            auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        except KeyError:
            logger.warning(
                "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
            )
            return [{"urls": ["stun:stun.l.google.com:19302"]}]

        client = Client(account_sid, auth_token)

        token = client.tokens.create()

        return token.ice_servers



    def main():
        st.header("Real Time Speech-to-Text")
        st.markdown(
            """
    This demo app is using [DeepSpeech](https://github.com/mozilla/DeepSpeech),
    an open speech-to-text engine.

    A pre-trained model released with
    [v0.9.3](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3),
    trained on American English is being served.
    """
        )

        # https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3
        MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"  # noqa
        LANG_MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"  # noqa
        MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.pbmm"
        LANG_MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.scorer"

        download_file(MODEL_URL, MODEL_LOCAL_PATH, expected_size=188915987)
        download_file(LANG_MODEL_URL, LANG_MODEL_LOCAL_PATH, expected_size=953363776)

        lm_alpha = 0.931289039105002
        lm_beta = 1.1834137581510284
        beam = 100

        sound_only_page = "Sound only (sendonly)"
        with_video_page = "With video (sendrecv)"
        app_mode = st.selectbox("Choose the app mode", [sound_only_page, with_video_page])

        if app_mode == sound_only_page:
            app_sst(
                str(MODEL_LOCAL_PATH), str(LANG_MODEL_LOCAL_PATH), lm_alpha, lm_beta, beam
            )
        elif app_mode == with_video_page:
            app_sst_with_video(
                str(MODEL_LOCAL_PATH), str(LANG_MODEL_LOCAL_PATH), lm_alpha, lm_beta, beam
            )


    def app_sst(model_path: str, lm_path: str, lm_alpha: float, lm_beta: float, beam: int):
        webrtc_ctx = webrtc_streamer(
            key="speech-to-text",
            mode=WebRtcMode.SENDONLY,
            audio_receiver_size=1024,
            rtc_configuration={"iceServers": get_ice_servers()},
            media_stream_constraints={"video": False, "audio": True},
        )

        status_indicator = st.empty()

        if not webrtc_ctx.state.playing:
            return

        status_indicator.write("Loading...")
        text_output = st.empty()
        stream = None

        while True:
            if webrtc_ctx.audio_receiver:
                if stream is None:
                    from deepspeech import Model

                    model = Model(model_path)
                    model.enableExternalScorer(lm_path)
                    model.setScorerAlphaBeta(lm_alpha, lm_beta)
                    model.setBeamWidth(beam)

                    stream = model.createStream()

                    status_indicator.write("Model loaded.")

                sound_chunk = pydub.AudioSegment.empty()
                try:
                    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
                except queue.Empty:
                    time.sleep(0.1)
                    status_indicator.write("No frame arrived.")
                    continue

                status_indicator.write("Running. Say something!")

                for audio_frame in audio_frames:
                    sound = pydub.AudioSegment(
                        data=audio_frame.to_ndarray().tobytes(),
                        sample_width=audio_frame.format.bytes,
                        frame_rate=audio_frame.sample_rate,
                        channels=len(audio_frame.layout.channels),
                    )
                    sound_chunk += sound

                if len(sound_chunk) > 0:
                    sound_chunk = sound_chunk.set_channels(1).set_frame_rate(
                        model.sampleRate()
                    )
                    buffer = np.array(sound_chunk.get_array_of_samples())
                    stream.feedAudioContent(buffer)
                    text = stream.intermediateDecode()
                    text_output.markdown(f"**Text:** {text}")
            else:
                status_indicator.write("AudioReciver is not set. Abort.")
                break


    def app_sst_with_video(
        model_path: str, lm_path: str, lm_alpha: float, lm_beta: float, beam: int
    ):
        frames_deque_lock = threading.Lock()
        frames_deque: deque = deque([])

        async def queued_audio_frames_callback(
            frames: List[av.AudioFrame],
        ) -> av.AudioFrame:
            with frames_deque_lock:
                frames_deque.extend(frames)

            # Return empty frames to be silent.
            new_frames = []
            for frame in frames:
                input_array = frame.to_ndarray()
                new_frame = av.AudioFrame.from_ndarray(
                    np.zeros(input_array.shape, dtype=input_array.dtype),
                    layout=frame.layout.name,
                )
                new_frame.sample_rate = frame.sample_rate
                new_frames.append(new_frame)

            return new_frames

        webrtc_ctx = webrtc_streamer(
            key="speech-to-text-w-video",
            mode=WebRtcMode.SENDRECV,
            queued_audio_frames_callback=queued_audio_frames_callback,
            rtc_configuration={"iceServers": get_ice_servers()},
            media_stream_constraints={"video": True, "audio": True},
        )

        status_indicator = st.empty()

        if not webrtc_ctx.state.playing:
            return

        status_indicator.write("Loading...")
        text_output = st.empty()
        stream = None

        while True:
            if webrtc_ctx.state.playing:
                if stream is None:
                    from deepspeech import Model

                    model = Model(model_path)
                    model.enableExternalScorer(lm_path)
                    model.setScorerAlphaBeta(lm_alpha, lm_beta)
                    model.setBeamWidth(beam)

                    stream = model.createStream()

                    status_indicator.write("Model loaded.")

                sound_chunk = pydub.AudioSegment.empty()

                audio_frames = []
                with frames_deque_lock:
                    while len(frames_deque) > 0:
                        frame = frames_deque.popleft()
                        audio_frames.append(frame)

                if len(audio_frames) == 0:
                    time.sleep(0.1)
                    status_indicator.write("No frame arrived.")
                    continue

                status_indicator.write("Running. Say something!")

                for audio_frame in audio_frames:
                    sound = pydub.AudioSegment(
                        data=audio_frame.to_ndarray().tobytes(),
                        sample_width=audio_frame.format.bytes,
                        frame_rate=audio_frame.sample_rate,
                        channels=len(audio_frame.layout.channels),
                    )
                    sound_chunk += sound

                if len(sound_chunk) > 0:
                    sound_chunk = sound_chunk.set_channels(1).set_frame_rate(
                        model.sampleRate()
                    )
                    buffer = np.array(sound_chunk.get_array_of_samples())
                    stream.feedAudioContent(buffer)
                    text = stream.intermediateDecode()
                    text_output.markdown(f"**Text:** {text}")
            else:
                status_indicator.write("Stopped.")
                break


    if __name__ == "__main__":
        import os

        DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]

        logging.basicConfig(
            format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
            "%(message)s",
            force=True,
        )

        logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

        st_webrtc_logger = logging.getLogger("streamlit_webrtc")
        st_webrtc_logger.setLevel(logging.DEBUG)

        fsevents_logger = logging.getLogger("fsevents")
        fsevents_logger.setLevel(logging.WARNING)

        main()
with col2:

    # This page is for chat
    from st_pages import add_page_title
    import const
    import datetime
    import os
    from PIL import Image
    import openai
    from streamlit_autorefresh import st_autorefresh
    from modules import common
    from modules.authenticator import common_auth
    from modules.database import database

    CHAT_ID = "0"
    CHAT_ID = st.text_input("ChatID")
    persona = None
    llm = None
    use_chatbot = False

    CHATBOT_PERSONA = """
    Please become a character of the following setting and have a conversation.

    {persona}
    """

    add_page_title()

    authenticator = common_auth.get_authenticator()
    db = database.Database()
    if (
        common.check_if_exists_in_session(const.SESSION_INFO_AUTH_STATUS)
        and st.session_state[const.SESSION_INFO_AUTH_STATUS]
    ):
        messages = []
        # Check if chatbot is enabled
        tmp_use_chatbot = db.get_openai_settings_use_character()
        if tmp_use_chatbot == 1:
            persona = db.get_character_persona()[0]
            messages.append(
                {"role": "system", "content": CHATBOT_PERSONA.format(persona=persona)}
            )

            # Get chatbot settings
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if openai_api_key is None:
                openai.api_key = openai_api_key
                persona = None
                st.error(
                    "OPENAI_API_KEY is not set in the environment variables. Please contact the administrator."
                )

        user_infos = {}
        username = st.session_state[const.SESSION_INFO_USERNAME]
        name = st.session_state[const.SESSION_INFO_NAME]

        # Show old chat messages
        chat_log = db.get_chat_log(chat_id=CHAT_ID, limit=const.MAX_CHAT_LOGS)
        if chat_log is not None:
            for msg_info in chat_log:
                log_chat_id, log_username, log_name, log_message, log_sent_time = msg_info
                # Get user info
                if log_username not in user_infos:
                    tmp_user_info = db.get_user_info(log_username)
                    if tmp_user_info is None:
                        st.error(const.ERR_MSG_GET_USER_INFO)
                    else:
                        user_infos[log_username] = {
                            "username": log_username,
                            "name": tmp_user_info[2],
                            "image_path": tmp_user_info[4],
                            "image": None,
                        }
                # Show chat message
                if log_username in user_infos:
                    if (
                        user_infos[log_username]["image"] is None
                        and user_infos[log_username]["image_path"] is not None
                        and os.path.isfile(user_infos[log_username]["image_path"])
                    ):
                        # Load user image
                        user_infos[log_username]["image"] = Image.open(
                            user_infos[log_username]["image_path"]
                        )
                    with st.chat_message(
                        log_name, avatar=user_infos[log_username]["image"]
                    ):
                        st.write(log_name + "> " + log_message)

                    if persona is not None:
                        # Added conversation to give to chatbot.
                        if log_username == const.CHATBOT_USERNAME:
                            messages.append({"role": "assistant", "content": log_message})
                        else:
                            messages.append(
                                {
                                    "role": "user",
                                    "content": log_name + " said " + log_message,
                                }
                            )
                        if len(messages) > const.MAX_CONVERSATION_BUFFER:
                            messages.pop(1)

        else:
            st.error(const.ERR_MSG_GET_CHAT_LOGS)

        # Show user message
        if user_msg:
            # Show new chat message
            db.insert_chat_log(
                chat_id=CHAT_ID,
                username=username,
                name=name,
                message=user_msg,
                sent_time=datetime.datetime.now(),
            )
            if username not in user_infos:
                # Get user info
                tmp_user_info = db.get_user_info(username)
                if tmp_user_info is None:
                    st.error(const.ERR_MSG_GET_USER_INFO)
                else:
                    user_infos[username] = {
                        "username": username,
                        "name": tmp_user_info[2],
                        "image_path": tmp_user_info[4],
                        "image": None,
                    }
            if (
                username in user_infos
                and user_infos[username]["image"] is None
                and user_infos[username]["image_path"] is not None
                and os.path.isfile(user_infos[username]["image_path"])
            ):
                user_infos[username]["image"] = Image.open(
                    user_infos[username]["image_path"]
                )
            with st.chat_message(name, avatar=user_infos[username]["image"]):
                st.write(name + "> " + user_msg)

            if persona is not None:
                # Show chatbot message
                messages.append({"role": "user", "content": name + " said " + user_msg})
                messages.append({"role": "assistant", "content": name + " said "})
                completion = openai.ChatCompletion.create(
                    model=const.MODEL_NAME,
                    messages=messages,
                )
                assistant_msg = completion["choices"][0]["message"]["content"]
                with st.chat_message(const.CHATBOT_NAME, avatar=const.CHATBOT_NAME):
                    st.write(const.CHATBOT_NAME + "> " + assistant_msg)
                db.insert_chat_log(
                    chat_id=CHAT_ID,
                    username=const.CHATBOT_USERNAME,
                    name=const.CHATBOT_NAME,
                    message=assistant_msg,
                    sent_time=datetime.datetime.now(),
                )

        # Refresh the page every (REFRESH_INTERVAL) seconds
        count = st_autorefresh(
            interval=const.REFRESH_INTERVAL, limit=None, key="fizzbuzzcounter"
        )
    else:
        st.error("You are not logged in. Please go to the login page.")

