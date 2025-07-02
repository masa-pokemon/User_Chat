import streamlit as st
from pytube import YouTube

st.title("YouTube Video Downloader")

video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    try:
        yt = YouTube(video_url)

        st.image(yt.thumbnail_url, caption="Video Thumbnail", width=300)
        st.write(f"**Title:** {yt.title}")
        st.write(f"**Views:** {yt.views:,}")

        # Get available streams
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        
        # Create a list of resolutions for the select box
        resolution_options = [s.resolution for s in streams if s.resolution]
        
        selected_resolution = st.selectbox("Select Resolution:", resolution_options)

        if st.button("Download Video"):
            selected_stream = None
            for s in streams:
                if s.resolution == selected_resolution:
                    selected_stream = s
                    break

            if selected_stream:
                st.info(f"Downloading '{yt.title}' at {selected_resolution}...")
                
                # Download to a temporary location or in-memory
                # For simplicity, let's download to a local file
                download_path = f"{yt.title}_{selected_resolution}.mp4"
                selected_stream.download(output_path='.', filename=download_path)
                
                st.success("Download complete!")

                # Provide a download button for the user
                with open(download_path, "rb") as file:
                    st.download_button(
                        label="Click to Download",
                        data=file.read(),
                        file_name=download_path,
                        mime="video/mp4"
                    )
            else:
                st.error("Could not find selected resolution.")

    except Exception as e:
        st.error(f"Error: {e}")
        st.error("Please check the URL or try again later.")
