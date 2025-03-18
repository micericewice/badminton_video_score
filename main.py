import sys, os
from config.config import CONFIGs
import util

import tkinter as tk
from tkinter import filedialog



def create_video_scoreboard(if_vid, scores_csv, bg_path, font, font_icon, of_vid):
   scores = util.parse_csv(scores_csv)
   return util.create_clip_overlay_all(if_vid, scores, bg_path, font, font_icon, of_vid)


def main(argv):
   root = tk.Tk()
   root.withdraw()
   if_vid = filedialog.askopenfilename(title="Select input video", initialdir="./in", filetypes=[('Video files', '*.mov *.mp4')], defaultextension='.mov')
   scores_csv = filedialog.askopenfilename(title="Select data", initialdir="./in", initialfile=f'{os.path.splitext(os.path.basename(if_vid))[0]}.csv', filetypes=[('CSV files', '*.csv')])
   of_vid = filedialog.asksaveasfilename(title="Save video as", initialdir="./out", initialfile=f'{os.path.splitext(os.path.basename(if_vid))[0]}.mp4', filetypes=[('Video files', '*.mp4')], defaultextension='.mp4')

   # if_vid = CONFIGs['input_video']
   # scores_csv = CONFIGs['score_csv']
   # of_vid = CONFIGs['output_video']
   png_dir = CONFIGs['png_dir']
   bg_path = CONFIGs['bg']
   font = CONFIGs['font']
   font_icon = CONFIGs['font_icon']
   video = create_video_scoreboard(if_vid, scores_csv, bg_path, font, font_icon, of_vid)
   util.export_output_video(video, of_vid)


if __name__ == '__main__':
   argv = sys.argv[1:]
   main(argv)
