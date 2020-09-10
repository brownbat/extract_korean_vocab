from konlpy.tag import Okt
from konlpy.tag import Kkma
import os
from google.cloud import translate_v2

# todo -- currently including redundant entires despite l46
# translates every word.
# slow. add progress bar.

# 1. install konlpy and confirm it's working (requires JDK)
# 2. get api creds json from google translate
# 3. install google cloud language
# 4. set your creds and java directories in the os.environ calls
# 5. set the in and out filenames below

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "g_creds.json"
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk-14.0.2"

in_filename = "singihan hangari.txt"
out_filename = "singihan out.txt"


translate_client = translate_v2.Client()
translate = translate_client.translate

okt = Okt()
kkma = Kkma()

vocab_list = []

def extract_korean_vocab(in_filename, out_filename):
    with open(in_filename, "r", encoding="utf-8") as korean_text_file_object:
        with open(out_filename, "w", encoding="utf-8") as outfile:
            story = korean_text_file_object.read()
            print("Splitting sentences...")
            sentences = kkma.sentences(story)
            print(f"Parsing words in {len(sentences)} sentences...")
            for sentence in sentences:
                tags = okt.pos(sentence, norm=True, stem=True)
                for t in tags:
                    if t[1] not in ['Foreign',
                                    'Punctuation',
                                    'Number',
                                    'Josa',
                                    'Eomi',
                                    'Suffix']:
                        if t[0] not in vocab_list:
                            vocab_list.append(t[0])
                            print(t[0])
                            proposed_entry = (t[0],
                                              translate(t[0])['translatedText'],
                                              t[1],
                                              sentence)
                            for f_idx, field in enumerate(proposed_entry):
                                outfile.write(str(field))
                                if f_idx < len(proposed_entry) - 1:
                                    outfile.write('|')
                                else:
                                    outfile.write('\n')
    print("Done!")

extract_korean_vocab(in_filename, out_filename)
