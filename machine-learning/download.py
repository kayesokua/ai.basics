from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytube
import time

credentials = service_account.Credentials.from_service_account_file('./keyfile.json')
youtube = build('youtube', 'v3', credentials=credentials)

def extract_video_from_youtube(query, count, output_dir):
    start_time = time.time()
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id',
        maxResults=count,
        order='relevance',
        relevanceLanguage='de',
        safeSearch='strict',
        videoDuration='short',
        regionCode='DE'
    ).execute()

    video_ids = [item['id']['videoId'] for item in search_response['items']]

    video_urls = ['https://www.youtube.com/watch?v=' + video_id for video_id in video_ids]

    i = 0
    for url in video_urls:
        try:
            video = pytube.YouTube(url)
            video_stream = video.streams.get_lowest_resolution()
            query_title = query.replace('+', '_')
            output_filename = f"{query_title}_{i}.mp4"
            video_stream.download(output_path=output_dir, filename=output_filename)
            print(f"{i}/{count} Downloaded")
            i += 1
        except KeyError:
            print(f"Error occurred while processing video {i}: {url}. Skipping.")
            continue

        if i >= count:
            break

    print(f"Downloaded {i} videos")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")


extract_video_from_youtube(query="solo+ballet", count=25, output_dir="train/")