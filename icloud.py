from pyicloud import PyiCloud

# Replace with your iCloud username (Apple ID) and password
username = 'your_email@example.com'
password = 'your_password'

# Initialize the iCloud API
api = PyiCloud(username, password)

# Get the photo and video library
photos = api.photos
videos = api.videos

# Set the local directory where you want to save the files
local_directory = '/path/to/local/directory/'

# Download photos
for photo in photos.all:
    photo.download(local_directory)

# Download videos
for video in videos.all:
    video.download(local_directory)

print("Download completed.")
