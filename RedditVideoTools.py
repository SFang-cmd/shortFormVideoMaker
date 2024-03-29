# Reddit Story Compiler with Interface
# By: Sean Fang

from TTSSys import *
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import RedditReader
import random
import math
import whisper_timestamped
import re
import os

# removing characters that might mess with the TikTokTTS API
def remove_non_ascii_1(text):
    return ''.join([i if ord(i) < 128 else '\'' for i in text])

def has_letters(text):
    for char in list(text):
        if ((ord(char) >= 41) and (ord(char) <= 90)) or ((ord(char) >= 97) and (ord(char) <= 122)):
            return True
    return False

    """Generates a twitter-style thumbnail for video
    :param pfp: The path to the profile picture
    :param name: The name of the user in the thumbnail
    :param tag_name: The @mention tag name of the user
    :param tag_addons: Any verified, emojis, or other 
    image file locations to add behind the name
    :param text: The body of the tweet style text
    :param output_path: The file to save the text in
    """
def draw_thumbnail(pfp, name, tag_name, tag_addons, text, output_path):
    # generates new image canvas
    image = Image.new("RGBA", (1280, 720), (0,0,0,0))
    # loads various images
    pfp_img = Image.open(pfp)
    verified_img = Image.open(tag_addons)
    icons_img = Image.open("thumbnailDets/twitter_icons.jpg")
    # creates a context instance
    draw = ImageDraw.Draw(image)
    # Loads up desired fonts
    name_font = ImageFont.truetype("fonts/verdanab.ttf", size=72)
    tag_font = ImageFont.truetype("Pillow/Tests/fonts/Verdana.ttf", size=60)
    text_font = ImageFont.truetype("fonts/verdanab.ttf", size=48)
    # processes text into lines of 42 with newlines separating them
    curr_char = 40
    text_length = len(text)
    total_lines = 0
    text_list = list(text)
    while curr_char < text_length:
        while text_list[curr_char] != ' ':
            curr_char -= 1
        text_list[curr_char] = "\n"
        total_lines += 1
        curr_char += 44
    text = "".join(text_list)
    # draws all of the elements onto the canvas
    draw.rounded_rectangle((0, 0, 1280, 720), fill="white", width=3, radius=50)
    image.paste(pfp_img, (75,75))
    draw.text((300,75), name, font=name_font, fill="black")
    image.paste(verified_img, (740,70))
    draw.text((320,160), tag_name, font=tag_font, fill="black")
    draw.multiline_text((75,(3-total_lines)*12 + 285), text, font=text_font, fill="black", spacing=10 + 5*(5-total_lines))
    image.paste(icons_img, (325,(total_lines-3)*30 + 575))
    # saves output
    image = image.resize(size=(405,228))
    image.save(output_path)


def generateVid(number, subreddit, time):
    # creates an instance of a reddit reader
    rr = RedditReader.redditReader()
    # gets the subreddit's top 5 posts
    subreddit = rr.getNewPost(subreddit=subreddit, mode="top", time=time, num_posts=number)
    # gets the first post of the subreddit
    for x in range(number):
        post = next(subreddit)
        print(post)
        print(vars(post))
        # Gather post details such as title and text
        title = remove_non_ascii_1(post.title)
        script = remove_non_ascii_1(post.selftext)

        # Generates a thumbnail
        draw_thumbnail("thumbnailDets/YTPFP.png", "PandaClan", "@Panda_Clan", "thumbnailDets/verified.png", title, "thumbnailDets/thumbnail_temp.png")

        # Clean posts and script so that the posts are processed for reading
        # Changes the letters AITA to Am I the A****** for reading
        title = re.sub('AITA', 'Am I the A-hole', title)
        # Changes date/letter combinations to hold a space between
        script = re.sub('(?<=\d)(?=[^\d\s])|(?<=[^\d\s])(?=\d)', ' ', script)
        # Changes the letters AITA to Am I the A*****
        script = re.sub('AITA', 'Am I the A-hole', script)
        script = re.sub('#', 'number', script)
        # Removes starting and trailing spaces
        script = script.strip()
        # splits the script into a list of segments that can be fed into the TTS system
        # note: this is necessary because the TTS can only process 300 tokens at a time,
        # so this is done to reduce the number of random pauses inside the reading
        list_script = re.split("[.!?]", script)

        # Chooses a voice to use
        voice = "en_us_010"
        # en_female_emotional
        # uses a tik tok text-to-speech api python wrapper to read out the title
        tts(title, voice, "tempAudioStorage/title.mp3", play_sound=True)
        # saves audio to file
        title_audio = AudioFileClip("tempAudioStorage/title.mp3")

        # feeds the tik tok tts api each sentence and saves the output to a file (in order)
        audio_list = []
        total_duration = 0
        sentenceNo = 1
        for sentence in list_script:
            in_sentence = sentence.strip()
            if (len(in_sentence) > 0) and has_letters(in_sentence): # To account for empty strings (since this will break the api)
                tts(in_sentence, voice, "tempAudioStorage/script" + str(sentenceNo) + ".mp3", play_sound=True)
                audio_list.append(AudioFileClip("tempAudioStorage/script" + str(sentenceNo) + ".mp3").set_start(total_duration,change_end=True))
                # Uses this to prevent all audio to be played immediately
                total_duration += (AudioFileClip("tempAudioStorage/script" + str(sentenceNo) + ".mp3")).duration
                sentenceNo += 1

        # Composites all the text audio together
        comp_audio = CompositeAudioClip(audio_list)
        # preps text audio to combine with title audio
        script_audio = comp_audio.set_start(title_audio.duration + 1)
        # combines all the audio together
        script_audio = CompositeAudioClip([title_audio, script_audio])
        # writes audio to file to prepare for caption processing
        script_audio.write_audiofile("tempAudioStorage/video_audio_temp.mp3",fps=44100)
        # computes the length of the total video so that background clip/music can be added
        length = title_audio.duration + total_duration + 1
        # loads background music
        music_audio = AudioFileClip("backgroundMusic/bgd2.mp3")
        if music_audio.duration > length:
            music_audio = music_audio.set_duration(length + 2)
        music_audio = music_audio.volumex(0.5)
        # composites the music onto the narration
        total_audio = CompositeAudioClip([title_audio, script_audio, music_audio])

        # loads background clip and thumbnail
        bgdClip = VideoFileClip("backgroundVids/background.mp4", audio=True)
        thumb_img = ImageClip("thumbnailDets/thumbnail_temp.png",transparent=True, duration=title_audio.duration)
        thumb_img = thumb_img.set_position(("center","center"))

        # chooses a random location to start the background clip and applies it to the clip
        clip_start = random.randint(0, math.floor(bgdClip.duration - length - 2))
        no_caption_clip = bgdClip.subclip(clip_start, clip_start + length + 2)

        # sets the audio to the reddit audio
        no_caption_clip = no_caption_clip.set_audio(total_audio)

        # Processes the speach to create captions using whisper_timestamped model
        model = whisper_timestamped.load_model("base")
        result = model.transcribe("tempAudioStorage/video_audio_temp.mp3",word_timestamps=True)
        segments = result["segments"]
        caption_list = []
        caption_list.append(no_caption_clip)
        caption_list.append(thumb_img)

        # Adds the timestamped words to the correct locations in the video
        for segment in segments:
            for word in segment["words"]:
                if title_audio.duration < word["start"]:
                    txt = (TextClip(word["word"], 
                                    fontsize=72,
                                    font=".SF-Compact-Bold", 
                                    stroke_color="black", 
                                    stroke_width=4,
                                    method="caption",
                                    color="white")
                                    .set_position(("center","center")))
                    txt_duration = word["end"] - word["start"]
                    txt = txt.set_duration(txt_duration)
                    txt = txt.set_start(word["start"])
                    txt = txt.set_position(("center","center"))
                    caption_list.append(txt)

        # saves the output file to a unique title in finalVids
        num_files = len(os.listdir("finalVids"))/2 + 1
        final_vid = CompositeVideoClip(caption_list)
        draw_thumbnail("thumbnailDets/YTPFP.png", "PandaClan", "@Panda_Clan", "thumbnailDets/verified.png", title, "finalVids/finalThumbnail" + str(num_files) + ".png")
        final_vid.write_videofile("finalVids/final" + str(num_files) + ".mp4", audio=True, audio_codec="aac")

        # remove all temporary files to clean the system
        for filename in os.listdir("tempAudioStorage"):
            os.remove("tempAudioStorage/" + filename)