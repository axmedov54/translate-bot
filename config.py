from gtts import gTTS

token = '7047365155:AAFt277J0GKrXGtrej57SgLOUqHj8gvkdAE'


def text_to_speech(mytext, lang):
    myobj = gTTS(text=mytext, lang=lang)
    myobj.save("audio.mp3")