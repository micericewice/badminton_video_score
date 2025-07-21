import csv
from moviepy import *
import os
from pprint import pprint

# consts
BG_W = 929
BG_H = 251
BG_OFFSET_FACTOR = 0.015 # 1.5% off original video height as offset top,left for the BG

PNAME_W = 650
PNAME_H = 90
PNAME_SIZE = PNAME_H - 30 # font size
PNAME_OFFSET_X = 30
PNAME_OFFSET_Y_1 = 30
PNAME_OFFSET_Y_2 = PNAME_OFFSET_Y_1 + 112

SHUTTLE_W = 100 # according to bg.png
SHUTTLE_H = 100 # according to bg.png
SHUTTLE_SIZE = SHUTTLE_H - 40 # font size
SHUTTLE_OFFSET_X = PNAME_OFFSET_X + PNAME_W
SHUTTLE_OFFSET_Y_1 = 24
SHUTTLE_OFFSET_Y_2 = SHUTTLE_OFFSET_Y_1 + 112

PSCORE_W = 143 # according to bg.png
PSCORE_H = 90 # according to bg.png
PSCORE_SIZE = PSCORE_H - 10 # font size
PSCORE_OFFSET_X = SHUTTLE_OFFSET_X + SHUTTLE_W + 2
PSCORE_OFFSET_Y_1 = 30
PSCORE_OFFSET_Y_2 = PSCORE_OFFSET_Y_1 + 112


def parse_csv(csv_file):
   ret = {}
   with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.reader(file, delimiter=',')

      row_count = 0
      row_header = next(reader)
      row_count += 1
      ret['pname1'] = row_header[2]
      ret['pname2'] = row_header[3]

      row_start = next(reader)
      row_count += 1
      start_sec = int(row_start[0]) * 60 + int(row_start[1])
      ret['start_sec'] = start_sec

      ret['pscore1'] = []
      ret['pscore2'] = []
      ret['serve_indicator'] = []
      pre_score_sec_p1 = start_sec
      pre_score_sec_p2 = start_sec
      pre_serve_indication_sec = start_sec
      score_p1 = int(row_start[2])
      score_p2 = int(row_start[3])
      last_scoring_player = "p1"

      # increments of scores
      for row in reader:
         row_count += 1
         timestamp_sec = int(row[0]) * 60 + int(row[1])
         if timestamp_sec<=pre_score_sec_p1 or timestamp_sec<=pre_score_sec_p2 or timestamp_sec<=pre_serve_indication_sec:
            raise Exception(f"timestamp is invalid at row {row_count}")
         ret['serve_indicator'] += [{
            'player' : last_scoring_player,
            'start' : pre_serve_indication_sec,
            'duration' : (timestamp_sec - pre_serve_indication_sec),
         }]
         pre_serve_indication_sec = timestamp_sec

         if row[2].strip().startswith(("x","X")): # p1 scored
            ret['pscore1'] += [{
               'start' : pre_score_sec_p1,
               'val' : score_p1,
               'duration' : (timestamp_sec - pre_score_sec_p1),
            }]
            score_p1 += 1
            pre_score_sec_p1 = timestamp_sec
            last_scoring_player = "p1"
         elif row[3].strip().startswith(("x","X")): # p2 scored
            ret['pscore2'] += [{
               'start' : pre_score_sec_p2,
               'val' : score_p2,
               'duration' : (timestamp_sec - pre_score_sec_p2),
            }]
            score_p2 += 1
            pre_score_sec_p2 = timestamp_sec
            last_scoring_player = "p2"
         else: # no on scored, this is end of the match
            ret['pscore1'] += [{
               'start' : pre_score_sec_p1,
               'val' : score_p1,
               'duration' : (timestamp_sec - pre_score_sec_p1),
            }]
            ret['pscore2'] += [{
               'start' : pre_score_sec_p2,
               'val' : score_p2,
               'duration' : (timestamp_sec - pre_score_sec_p2),
            }]
            ret['end_sec'] = timestamp_sec


   # pprint(ret, sort_dicts=False)
   return ret


def get_org_video_size(if_vid):
   w,h = (0,0)
   with VideoFileClip(if_vid) as v:
      w,h = v.size
   print(f'original video: {w}x{h}')
   return w,h


# load orginal video as Clip
def create_clips_org_video(if_vid):
   ret = []
   clip_org_vid = VideoFileClip(if_vid)
   ret.append(clip_org_vid)
   return ret


# create ImageClip of score board with time = final video time
def create_clips_bg(bg_path, video_w, video_h, scale):
   ret = []
   clip_bg = ImageClip(bg_path)
   clip_bg = clip_bg.resized(height=int(BG_H*scale))
   clip_bg = clip_bg.with_position((video_h*BG_OFFSET_FACTOR, video_h*BG_OFFSET_FACTOR))
   ret.append(clip_bg)
   return ret


# create TextClip of pname1 with time = final video time
# create TextClip of pname2 with time = final video time
def create_clips_pname(name, font, video_w, video_h, scale, pid):
   ret = []
   clip_pname = TextClip(
      font=font,
      text=name,
      method='label',
      size=(PNAME_W, PNAME_H),
      font_size=PNAME_SIZE,
      color='#222222',
      text_align='center',
      horizontal_align='center',
      vertical_align='center',
      duration=None,
   )
   offset_y = PNAME_OFFSET_Y_1 if pid==1 else PNAME_OFFSET_Y_2
   clip_pname = clip_pname.resized(height=int(PNAME_H*scale))
   clip_pname = clip_pname.with_position((
      PNAME_OFFSET_X*scale + video_h*BG_OFFSET_FACTOR,
      offset_y*scale + video_h*BG_OFFSET_FACTOR
   ))
   ret.append(clip_pname)
   return ret


# create multiple TextClip for scores of Player 01, add slide in/out from left->right if possible
# create multiple TextClip for scores of Player 02, add slide in/out from left->right if possible
def create_clips_pscores(data, font, video_w, video_h, scale, pid):
   ret = []
   for item in data:
      clip_score = TextClip(
         font=font,
         text=str(item['val']),
         method='label',
         size=(PSCORE_W, PSCORE_H),
         font_size=PSCORE_SIZE,
         color='#dddddd',
         text_align='center',
         horizontal_align='center',
         vertical_align='center',
         duration=item['duration'],
      )
      clip_score = clip_score.resized(height=int(PSCORE_H*scale))
      offset_y = PSCORE_OFFSET_Y_1 if pid==1 else PSCORE_OFFSET_Y_2
      clip_score = clip_score.with_position((
         PSCORE_OFFSET_X*scale + video_h*BG_OFFSET_FACTOR,
         offset_y*scale + video_h*BG_OFFSET_FACTOR
      ))
      clip_score = clip_score.with_start(item['start'])
      ret.append(clip_score)
   return ret


# create ImageClip of score board with time = final video time
def create_clips_serve(data, font_icon, video_w, video_h, scale):
   ret = []
   for item in data:
      clip_serve = TextClip(
         font=font_icon,
         text='\uf04b',
         method='label',
         size=(SHUTTLE_W, SHUTTLE_H),
         font_size=SHUTTLE_SIZE,
         color='#995238',
         text_align='center',
         horizontal_align='right',
         vertical_align='center',
         duration=item['duration'],
         margin=(10,10),
      )
      clip_serve = clip_serve.resized(height=int(SHUTTLE_H*scale))
      offset_y = SHUTTLE_OFFSET_Y_1 if item['player']=='p1' else SHUTTLE_OFFSET_Y_2
      clip_serve = clip_serve.with_position((
         SHUTTLE_OFFSET_X*scale + video_h*BG_OFFSET_FACTOR,
         offset_y*scale + video_h*BG_OFFSET_FACTOR
      ))
      clip_serve = clip_serve.with_start(item['start'])
      ret.append(clip_serve)
   return ret


# Overlay all clips together
def create_clip_overlay_all(if_vid, scores_data, bg_path, font, font_icon, out_vid):
   video_w,video_h = get_org_video_size(if_vid)
   scale = video_h*0.1 / BG_H
   all_clips = []
   all_clips += create_clips_org_video(if_vid)
   all_clips += create_clips_bg(bg_path, video_w, video_h, scale)
   all_clips += create_clips_pname(scores_data['pname1'], font, video_w, video_h, scale, pid=1)
   all_clips += create_clips_pname(scores_data['pname2'], font, video_w, video_h, scale, pid=2)
   all_clips += create_clips_pscores(scores_data['pscore1'], font, video_w, video_h, scale, pid=1)
   all_clips += create_clips_pscores(scores_data['pscore2'], font, video_w, video_h, scale, pid=2)
   all_clips += create_clips_serve(scores_data['serve_indicator'], font_icon, video_w, video_h, scale)
   final_clip = CompositeVideoClip(all_clips).subclipped(scores_data['start_sec'],scores_data['end_sec'])
   return final_clip


def preview_output_video(final_clip):
   final_clip.preview()


def export_output_video(final_clip, of_vid):
   final_clip.write_videofile(of_vid)


# In a CompositionClip, each clip start to play at a time that is specified by his clip.start attribute, and will play until clip.end.

# So, considering that you would want to play clip1 for the first 6 seconds, clip2 5 seconds after the start of the video, and finally clip3 at the end of clip2, you would do as follows:

# from moviepy import VideoFileClip, CompositeVideoClip

# # We load all the clips we want to compose
# clip1 = VideoFileClip("example.mp4")
# clip2 = VideoFileClip("example2.mp4").subclipped(0, 1)
# clip3 = VideoFileClip("example3.mp4")

# # We want to stop clip1 after 1s
# clip1 = clip1.with_end(1)

# # We want to play clip2 after 1.5s
# clip2 = clip2.with_start(1.5)

# # We want to play clip3 at the end of clip2, and so for 3 seconds only
# # Some times its more practical to modify the duration of a clip instead
# # of his end
# clip3 = clip3.with_start(clip2.end).with_duration(1)

# # We write the result
# final_clip = CompositeVideoClip([clip1, clip2, clip3])
# final_clip.write_videofile("final_clip.mp4")

# Note

# When working with timing of your clip, you will frequently want to keep only parts of the original clip. To do so, you should take a look at subclipped() and with_section_cut_out().



