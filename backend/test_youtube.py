from app.services.youtube import download_youtube_audio

if __name__ == "__main__":
    path, title = download_youtube_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Downloaded: {title}")
    print(f"Saved to: {path}")