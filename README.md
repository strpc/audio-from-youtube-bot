# audio-from-youtube-bot


## Description
Telegram bot, which sends a file(audio/video) via a link to [youtube](youtube.com)(to listen/view offline in the future). 


## Install
```sh
git clone https://github.com/strpc/audio-from-youtube-bot.git
cd audio-from-youtube-bot
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
brew install ffmpeg/apt-get install ffmpeg
add your telegram token to config.py
python3 bot.py
```


## Add conf for supervisor
```sh
[program:audio-from-youtube-bot]
command=/audio-from-youtube-bot/venv/bin/python3 -u /audio-from-youtube-bot/bot.py
directory=/audio-from-youtube-bot/yt_bot/
autostart=true
autorestart=true
stopsignal=KILL
numprocs=1
stdout_logfile=/audio-from-youtube-bot/log_supervisor.txt
redirect_stderr=true
```
```supervisorctl reread```

```supervisorctl reload```

```supervisorctl status audio-from-youtube-bot```
