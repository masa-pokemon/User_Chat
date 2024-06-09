# This page is for chat
import streamlit as st
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
import logging
import math
import urllib.request
from pathlib import Path
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
user_msg = st.chat_input("Enter your message")
col1, col2 = st.columns(2)
with col1:
    
    logger = logging.getLogger(__name__)

    cv2_path = Path(cv2.__file__).parent


    def imread_from_url(url: str):
        req = urllib.request.urlopen(url)
        encoded = np.asarray(bytearray(req.read()), dtype="uint8")
        image_bgra = cv2.imdecode(encoded, cv2.IMREAD_UNCHANGED)

        return image_bgra


    def overlay_bgra(background: np.ndarray, overlay: np.ndarray, roi):
        roi_x, roi_y, roi_w, roi_h = roi
        roi_aspect_ratio = roi_w / roi_h

        # Calc overlay x, y, w, h that cover the ROI keeping the original aspect ratio
        ov_org_h, ov_org_w = overlay.shape[:2]
        ov_aspect_ratio = ov_org_w / ov_org_h

        if ov_aspect_ratio >= roi_aspect_ratio:
            ov_h = roi_h
            ov_w = int(ov_aspect_ratio * ov_h)
            ov_y = roi_y
            ov_x = int(roi_x - (ov_w - roi_w) / 2)
        else:
            ov_w = roi_w
            ov_h = int(ov_w / ov_aspect_ratio)
            ov_x = roi_x
            ov_y = int(roi_y - (ov_h - roi_h) / 2)

        resized_overlay = cv2.resize(overlay, (ov_w, ov_h))

        # Cut out the pixels of the overlay image outside the background frame.
        margin_x0 = -min(0, ov_x)
        margin_y0 = -min(0, ov_y)
        margin_x1 = max(background.shape[1], ov_x + ov_w) - background.shape[1]
        margin_y1 = max(background.shape[0], ov_y + ov_h) - background.shape[0]

        resized_overlay = resized_overlay[
            margin_y0 : resized_overlay.shape[0] - margin_y1,
            margin_x0 : resized_overlay.shape[1] - margin_x1,
        ]
        ov_x += margin_x0
        ov_w -= margin_x0 + margin_x1
        ov_y += margin_y0
        ov_h -= margin_y0 + margin_y1

        # Overlay
        foreground = resized_overlay[:, :, :3]
        mask = resized_overlay[:, :, 3]

        overlaid_area = background[ov_y : ov_y + ov_h, ov_x : ov_x + ov_w]
        overlaid_area[:] = np.where(mask[:, :, np.newaxis], foreground, overlaid_area)


    class FaceOverlayProcessor(VideoProcessorBase):
        filter_type: Literal["none","ironman", "laughing_man", "cat"]

        def __init__(self) -> None:
            self._face_cascade = cv2.CascadeClassifier(
                str(cv2_path / "data/haarcascade_frontalface_alt2.xml")
            )

            self.filter_type = "ironman"
            self._filters = { 
                "none" : imread_from_url(
                    "https://drive.google.com/file/d/1CeaTD5RI6lvnha6XcuJFP3Cf1TMiYagg/view?usp=share_link"
                ),
                "ironman": imread_from_url(
                    "https://i.pinimg.com/originals/0c/c0/50/0cc050fd99aad66dc434ce772a0449a9.png"  # noqa: E501
                ),
                "laughing_man": imread_from_url(
                    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/3a17e5a4-9610-4fa3-a4bd-cb7d94d6f7e1/darwcty-d989aaf1-3cfa-4576-b2ac-305209346162.png/v1/fill/w_944,h_847,strp/laughing_man_logo_by_aggressive_vector_darwcty-pre.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9OTE5IiwicGF0aCI6IlwvZlwvM2ExN2U1YTQtOTYxMC00ZmEzLWE0YmQtY2I3ZDk0ZDZmN2UxXC9kYXJ3Y3R5LWQ5ODlhYWYxLTNjZmEtNDU3Ni1iMmFjLTMwNTIwOTM0NjE2Mi5wbmciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.5SDBnNZF6ktZM7Mk5gJfpHNQswRba3eqpvUn6FMHyW4"  # noqa: E501
                ),
                "cat": imread_from_url(
                    "https://i.pinimg.com/originals/29/cd/fd/29cdfdf2248ce2465598b2cc9e357579.png"  # noqa: E501
                ),
            }

            self.draw_rect = False  # For debug

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = self._face_cascade.detectMultiScale(
                gray, scaleFactor=1.11, minNeighbors=3, minSize=(30, 30)
            )

            overlay = self._filters[self.filter_type]

            for (x, y, w, h) in faces:
                # Ad-hoc adjustment of the ROI for each filter type
                if self.filter_type == "none":
                    roi = (x, y, int(0 * 1.15), 0)
                elif self.filter_type == "ironman":
                    roi = (x, y, w, h)
                elif self.filter_type == "laughing_man":
                    roi = (x, y, int(w * 1.15), h)
                elif self.filter_type == "cat":
                    roi = (x, y - int(h * 0.3), w, h)
                overlay_bgra(img, overlay, roi)

                if self.draw_rect:
                    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

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
                iserver_state["webrtc_contexts"] = []

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
                    processor_factory=FaceOverlayProcessor,
                )
                mix_track.add_input_track(self_process_track)

                self_process_track.processor.filter_type = st.radio(
                    "Select filter type",
                    ("none", "ironman", "laughing_man", "cat"),
                    key="filter-type",
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
                    video = st.checkbox('video')
                    audio = st.checkbox('audio')
                    media_stream_constraints={"video": video, "audio": audio},
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
    CHAT_ID = "0"
    CHAT_ID = st.text_input("Enter your message")
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
