from pydub import AudioSegment
from pydub.playback import play

def buzz():
    try:
        sound = AudioSegment.from_mp3("./sound/ascend.mp3")
        play(sound)
    except Exception as e:
        print("error  %d: %s" % (e.args[0], e.args[1]))
        raise
    

