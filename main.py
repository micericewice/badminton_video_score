import sys, os
from config.config import CONFIGs
import util
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from pprint import pprint



def create_video_scoreboard(if_vid, scores_sheet, bg_path, font, font_icon, of_vid):
   ext = Path(scores_sheet).suffix
   if ext.lower()==".csv":
      scores = util.parse_csv(scores_sheet)
   elif ext.lower()==".xlsx":
      scores = util.parse_xlsx(scores_sheet)
   else: raise Exception(f"{ext} is not supported!")
   # pprint(scores)
   return util.create_clip_overlay_all(if_vid, scores, bg_path, font, font_icon, of_vid)


def main(argv):
   root = tk.Tk()
   root.withdraw()
   if_vid = filedialog.askopenfilename(
      title="Select input video",
      initialdir="./in",
      filetypes=[('Video files', '*.mov *.mp4')],
      defaultextension='.mov')
   scores_sheet = filedialog.askopenfilename(
      title="Select data",
      initialdir="./in",
      initialfile=f'{os.path.splitext(os.path.basename(if_vid))[0]}.xlsx',
      filetypes=[('CSV, XLSX files', '*.csv *.xlsx')])
   of_vid = filedialog.asksaveasfilename(
      title="Save video as",
      initialdir="./out",
      initialfile=f'{os.path.splitext(os.path.basename(if_vid))[0]}.mp4',
      filetypes=[('Video files', '*.mp4')],
      defaultextension='.mp4')
   png_dir = CONFIGs['png_dir']
   bg_path = CONFIGs['bg']
   font = CONFIGs['font']
   font_icon = CONFIGs['font_icon']
   video = create_video_scoreboard(if_vid, scores_sheet, bg_path, font, font_icon, of_vid)
   util.export_output_video(video, of_vid)


if __name__ == '__main__':
   argv = sys.argv[1:]
   main(argv)
