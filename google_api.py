import os
import googleapiclient.discovery
from google.oauth2 import service_account
# Import datetime module
import datetime

# Define API service name and version
api_service_name = "youtube"
api_version = "v3"

# Load the service account credentials from the JSON key file
creds = service_account.Credentials.from_service_account_file(
    'vertical-album-383200-efc0b266833b.json',
    scopes=['https://www.googleapis.com/auth/youtube']
)
print(vars(creds))

# Create the API client using the service account credentials
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=creds)


# Define a function to delete all videos uploaded today except the most recent one
def delete_videos():
    # Get today's date and time in the EST time zone
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))

    # Convert today's date and time to ISO format and adjust the time zone to UTC
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(datetime.timezone.utc).isoformat()
    today_end = now.astimezone(datetime.timezone.utc).isoformat()

    # Get all the video IDs uploaded today except the most recent one
    request = youtube.search().list(
        part="id",
        type="video",
        channelId="UCioh9Wq_z825232pIKsGZyA",
        maxResults=50,
        order="date",
        publishedAfter=today_start,
        publishedBefore=today_end,
    )
    response = request.execute()
    print(response)
    video_ids = [item["id"] for item in response["items"][1:]]
    print(video_ids)

    # Delete each video one by one
    for video_id in video_ids:
        request = youtube.videos().delete(
            id=video_id['videoId']
        )
        response = request.execute()
        print(response)
        print(f"Deleted video {video_id['videoId']}")


# Define a function to list today's videos
def list_today_videos():
    # Get today's date and time in the EST time zone
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))

    # Convert today's date and time to ISO format and adjust the time zone to UTC
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(datetime.timezone.utc).isoformat()
    today_end = now.astimezone(datetime.timezone.utc).isoformat()

    # Call the API to list the videos uploaded today
    request = youtube.search().list(
        part="id,snippet",
        type="video",
        channelId="UCioh9Wq_z825232pIKsGZyA",
        maxResults=50,
        publishedAfter=today_start,
        publishedBefore=today_end,
        order="date"
    )
    response = request.execute()

    # Print the title and URL of each video
    for item in response["items"]:
        print(item["snippet"]["title"])
        print("https://www.youtube.com/watch?v=" + item["id"]["videoId"])
        print()

if __name__ == '__main__':
    # Call the list_today_videos function
    delete_videos()
    list_today_videos()
