import streamlit as st
from pytube import YouTube

st.title("YouTube Video Downloader")

video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    try:
        yt = YouTube(video_url)

        st.image(yt.thumbnail_url, caption="Video Thumbnail")
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Views:** {yt.views:,}")
        st.write(f"**Length:** {yt.length // 60} minutes {yt.length % 60} seconds")

        # Filter for available streams (e.g., progressive, mp4)
        # You might want to offer different quality options to the user
        available_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

        if available_streams:
            st.subheader("Available Resolutions:")
            resolution_options = [s.resolution for s in available_streams if s.resolution]
            selected_resolution = st.selectbox("Select Resolution:", resolution_options)

            if st.button("Download Video"):
                with st.spinner("Downloading..."):
                    # Get the stream for the selected resolution
                    selected_stream = available_streams.filter(resolution=selected_resolution).first()
                    if selected_stream:
                        selected_stream.download()
                        st.success("Download Complete!")
                        st.balloons()
                    else:
                        st.error("Could not find selected stream.")
        else:
            st.warning("No progressive MP4 streams available for this video.")

    except Exception as e:
        st.error(f"Error: {e}")
        st.warning("Please make sure the URL is valid and the video is not age-restricted or unavailable.")
