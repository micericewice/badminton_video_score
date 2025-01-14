# Description
From recorded video of badminton game (or similar sports),
overlay the scoreboard with scores updated during the video time

# Install required python modules
    python -m pip install -r requirements.txt

# Config the tool
## Put input video to ./in/ folder
Example: ./in/video.mov

## update ./in/score.csv
| Min | Sec | P1_name | P2_name ||
| --- | --- | :---: | :---: ||
|0|5|0|0| <i>0m5s the game starts, 0-0 is starting score</i> |
|0|10|x|| <i>0m10s P1 scores, update scoreboard as 1-0</i> |
|0|17||x| <i>0m17s P2 scores, update scoreboard as 1-1</i> |
|10|0||| <i> 10m0s, no one scores, end the video here</i> |

## update ./config/config.py
customize config.py if needed, ex:<br>
    - 'input_video'<br>
    - 'output_video'


# Create new video with scoreboard updated
    create_scoreboard_video.cmd
