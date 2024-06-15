
import streamlit as st
user_msg = st.chat_input("Enter your message")
col1, col2 = st.columns(2)
i = None
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
                i = ctx.state.playing
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


st.write(i)
