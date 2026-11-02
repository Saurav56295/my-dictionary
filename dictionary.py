import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
def look_up_word(word):
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + quote(word)
    request = Request(url, headers={"User-Agent": "PythonDictionary/1.0"})
    try:
        with urlopen(request, timeout=10) as response:
            entries = json.loads(response.read().decode("utf-8"))
        return entries
    except HTTPError as error:
        if error.code == 404:
            return []
        raise
print("Welcome to the Dictionary!")
print("Type a word to look it up, or type 'quit' to exit.")
while True:
    word = input("\nEnter a word: ").strip()
    if word.lower() == "quit":
        print("Goodbye!")
        break
    if word == "":
        print("Please enter a word.")
        continue
    try:
        entries = look_up_word(word)
        if len(entries) == 0:
            print("No meaning found for '{}'. Check the spelling.".format(word))
            continue
        pronunciation = ""
        for entry in entries:
            for phonetic in entry.get("phonetics", []):
                pronunciation = phonetic.get("text", "")
                if pronunciation != "":
                    break
            if pronunciation != "":
                break
        if pronunciation != "":
            print("\nPronunciation: {}".format(pronunciation))
        else:
            print("\nPronunciation is not available.")
        print("\nMeanings and examples:")
        number = 1
        for entry in entries:
            for meaning in entry.get("meanings", []):
                part_of_speech = meaning.get("partOfSpeech", "word")
                for definition in meaning.get("definitions", []):
                    meaning_text = definition.get("definition", "")
                    print("{}. ({}) {}".format(number, part_of_speech, meaning_text))
                    example = definition.get("example", "")
                    if example != "":
                        print("   Example: {}".format(example))
                    number = number + 1
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        print("Could not reach the dictionary service: {}".format(error))