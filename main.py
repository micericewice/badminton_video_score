import sys
from config.config import CONFIGs
import util


def create_video_scoreboard(if_vid, scores_csv, bg_path, font, of_vid):
   scores = util.parse_csv(scores_csv)
   return util.create_clip_overlay_all(if_vid, scores, bg_path, font, of_vid)


def main(argv):
   scores_csv = CONFIGs['score_csv']
   if_vid = CONFIGs['input_video']
   of_vid = CONFIGs['output_video']
   png_dir = CONFIGs['png_dir']
   bg_path = CONFIGs['bg']
   font = CONFIGs['font']
   video = create_video_scoreboard(if_vid, scores_csv, bg_path, font, of_vid)
   util.export_output_video(video, of_vid)


if __name__ == '__main__':
   argv = sys.argv[1:]
   main(argv)
