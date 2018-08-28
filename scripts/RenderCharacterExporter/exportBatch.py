import renderCharExporter as rce
import json
dataPath = '../DataFiles/export_char_list.json'

def getCharacters():

    with open(dataPath) as dataFile:
        data = json.load(dataFile)
    return data['Characters']

def main():
    characters = getCharacters()

    for character in characters:
        rce.main(character)

main()