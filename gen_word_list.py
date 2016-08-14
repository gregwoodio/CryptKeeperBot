# gen_word_list.py
# Thanks to RhymeBrain.com for the use of their API.

import requests
import sys
import time

def main():
    if len(sys.argv) != 4:
        print('Usage: gen_word_list.py <input file> <output file> <tolerance 0-300>\n')
        return 1

    file_input = open(sys.argv[1], 'r');
    tolerance = int(sys.argv[3]);
    if tolerance < 0:
        tolerance = 0
    elif tolerance > 300:
        tolerance = 300

    # get scary words
    scary_words = file_input.read().splitlines()

    # make our rhyming dictionary using Rhymebrain
    rhyme_dict = {}
    url = 'http://rhymebrain.com/talk'

    for scary_word in scary_words:
        params = {
                'function': 'getRhymes',
                'word': scary_word,
                'lang': 'en'
        }
        req = requests.get(url, params)
        
        for word in req.json():
            if word['score'] > tolerance:
                if word['word'] not in rhyme_dict:
                    rhyme_dict[word['word']] = []

                rhyme_dict[word['word']].append(scary_word)
        # delay a bit for rate limiting
        time.sleep(5)

    print(rhyme_dict)

    # output our rhyming dictionary to a file
    file_output = open(sys.argv[2], 'w');
    file_output.write('# Rhyming dictionary\n\n')
    file_output.write('rhyme_dict = {\n')
    for word in rhyme_dict:
        file_output.write('\t\'' + word + '\': [\n')
        for rhyme in rhyme_dict[word]:
            file_output.write('\t\t\'' + rhyme + '\',\n')
        file_output.write('\t],\n')
    file_output.write('}')
    file_output.close()

if __name__ == '__main__':
    main()
