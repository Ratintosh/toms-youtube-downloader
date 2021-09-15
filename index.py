from flask import Flask, request, send_file, render_template
from pytube import YouTube
import os
import subprocess
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submitData', methods=('GET', 'POST'))
def create():
    #clean up the directory a lil bit (will return an error if nothings there, hopefully it shouldn't cause the program to break)
    subprocess.run(['rm', 'cache/*'])
    subprocess.run(['rm', 'cache/*'])
    url=request.form.get('url')
    yt=YouTube(url)
    ytst=yt.streams.filter(only_audio=True)
    ys=yt.streams.get_by_itag('140') #i assume itag140 is audio in .mp4 format? i hope it doesnt differ on URLs
    title=yt.title
    title=title.replace('.','')
    filename=title+'.mp4'
    ys.download('cache')
    print(ys)
    subprocess.run(['ffmpeg','-i', 'cache/'+filename, 'cache/'+title+'.mp3', '-y'])
    #wait what happens when the video is a 404? does the site crash?
    return send_file('cache/'+title+'.mp3', as_attachment=True)
    #clear cache (dunno if this will run, since its after the return statement)
    subprocess.run(['rm', 'cache/*'])
    subprocess.run(['rm', 'cache/*'])

#idk if this is helpful or not
class TestFailed(Exception):
    pass
