from flask import Flask, render_template, request, jsonify, send_file, url_for, redirect
from pytube import YouTube

app = Flask(__name__)

def lenght_converter(x):
        length_minutes = x // 60
        x %= 60
        length_formatted = f"{length_minutes} min {x} sec"
        return length_formatted

@app.route('/')
def redirects():
    return redirect(url_for('home'))
    

@app.route('/yt-downloader', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        youtube_url = request.form['VidURL']

        if youtube_url:

            try:

                yt = YouTube(youtube_url)

                # Video Details
                title = yt.title
                thumbnail = yt.thumbnail_url
                views = yt.views
                vid_length = yt.length
                get_result_video_length = lenght_converter(vid_length)
                
                # Get Video Resolution
                youtubeObject = yt.streams.filter(progressive=True)

                stream_data = []

                for stream in youtubeObject:
                    if stream.type == 'video':
                        stream_info = {
                            "itag": stream.itag,
                            "mime_type": stream.mime_type,
                            "res": stream.resolution,
                            "type": stream.type
                        }
                        stream_data.append(stream_info)
                        print(stream_data)

                return render_template('yt-downloader.html', title=title, thumbnail=thumbnail, length=get_result_video_length , views=views, stream_data=stream_data, youtube_url=youtube_url)
            
            except:
                error = "Invalid Format"
                return render_template('yt-downloader.html', error=error)

        else:
            print('Invalid')

    return render_template('yt-downloader.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        selected_itag = request.json.get('tagValues')
        vidURL = request.json.get('vidURL')
        
        if selected_itag == "Select Video Resolutions":
            print('Select A Value')

        else:
            print(selected_itag)
            sent_video_downloaded = get_videodownloaded(vidURL, selected_itag)
            video_file_path = sent_video_downloaded
            return send_file(video_file_path, as_attachment=True)

        return jsonify({'message': f'Downloading video with this itag {selected_itag}'})

    return jsonify({'error': 'Invalid request'})

def get_videodownloaded(l,r):

    yt = YouTube(l)
    stream = yt.streams.get_by_itag(r)
    vid = stream.download(output_path='static/vid', filename=f'{yt.title}.mp4', skip_existing=True, max_retries=0)
    return vid

if __name__ == '__main__':
    app.run(debug=True)
