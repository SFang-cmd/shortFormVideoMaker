# Import everything needed to edit video clips
from moviepy.editor import *
import RedditReader

bgdClip = "background.mov"
script = "This is my test script"


rr = RedditReader.redditReader("7pQOH7DGpC8RnPP-0vGL8Q", "	bl1ScELhHOUi-IuswvcCkwgMWrRK4Q", "User-Agent: mac:com.beanboi9001.redditstoryscript:v1.0 (by /u/beanboi9001)")

print(rr.isReadOnly())










# # import moviepy
# # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60

# clip = VideoFileClip("memes.mov").subclip(30,40)

# # Generate a text clip. You can customize the font, color, etc.
# txt_clip = TextClip("My Holidays 2013",fontsize=70,color='white')

# # Say that you want it to appear 10s at the center of the screen
# txt_clip.set_position('center')
# txt_clip.set_duration(10)

# # Overlay the text clip on the first video clip
# video = CompositeVideoClip([clip, txt_clip])
# video.duration = 10

# # Write the result to a file (many options available !)
# video.write_videofile("editTest.mp4")