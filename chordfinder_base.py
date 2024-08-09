# ChordFinder by Raj Esakimuthu
# A Program that results a set of chords, the order to play them, and what to play on each hand according to the tune the user inputs from a section of a song

# Imports Pymongo with MongoClient, and Certifi
from pymongo import MongoClient
import certifi

# Asks the User the notes of the tune section they want chords for and places that input into a list
tune_notes = []
enter_notes = input("Enter Notes of the Tune Section (Hook, Verse, Bridge) (Ex. A,A#,A-flat): ")
tune_notes = enter_notes.split(",")

for i in range(len(tune_notes)):
    if tune_notes[i] == "A-flat":
        tune_notes[i] = "G#"
    elif tune_notes[i] == "B-flat":
        tune_notes[i] = "A#"
    elif tune_notes[i] == "C-flat":
        tune_notes[i] = "B"
    elif tune_notes[i] == "D-flat":
        tune_notes[i] = "C#"
    elif tune_notes[i] == "E-flat":
        tune_notes[i] = "D#"
    elif tune_notes[i] == "F-flat":
        tune_notes[i] = "E"
    elif tune_notes[i] == "G-flat":
        tune_notes[i] = "F#"
    elif tune_notes[i] == "B#":
        tune_notes[i] = "C"
    elif tune_notes[i] == "E#":
        tune_notes[i] = "F"

scales = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
minor_third_notes = ["D#","E","F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D"]

# Function that recurs through the list of the tune notes and finds and prints out the scale of the tune

def scale(notes):
    tune_scale = ""
    for j in range(len(scales)):
        if tune_notes[-1] == scales[j]:
            if minor_third_notes[j] in tune_notes:
                tune_scale = f'{scales[j]} Minor'
            else:
                tune_scale = f'{scales[j]} Major'
    return tune_scale

song_scale = scale(tune_notes)

# Makes sure names of the scale are accurate

if song_scale == "F# Major":
    song_scale = "G-flat Major"
elif song_scale == "C# Major":
    song_scale = "D-flat Major"
elif song_scale == "G# Major":
    song_scale = "A-flat Major"
elif song_scale == "D# Major":
    song_scale = "E-flat Major"
elif song_scale == "A# Major":
    song_scale = "B-flat Major"
elif song_scale == "A# Minor":
    song_scale = "B-flat Minor"
elif song_scale == "D# Minor":
    song_scale = "E-flat Minor"

if song_scale[-3:] == "nor":
    is_minor = True
elif song_scale[-3:] == "jor":
    is_major = True

print_scale = print(f'SCALE: {song_scale}')

try_new_chord = "Y"

# While loop to repeat the process of the program in the case the user wants to find a different type of chord other than the one they chose

while try_new_chord == "Y":

    # Asks user which type of chord they would like for their tune
    chord_type = input("Which type of Chords would you like (Triad, Bright Triad, Augmented, Diminished, Dominant 7th)?: ")

    # Prevents errors if the user chooses options that are not valid or possible in the program
    while chord_type == "Augmented" and is_minor == True:
        chord_type = input("NOT VALID: Choose a different type of chord (Triad, Bright Triad, Augmented, Diminished, Dominant 7th)?: ")
    while chord_type == "Diminished" and is_major == True:
        chord_type = input("NOT VALID: Choose a different type of chord (Triad, Bright Triad, Augmented, Diminished, Dominant 7th)?: ")
    while chord_type =="Dominant 7th" and is_minor == True:
        chord_type = input("NOT VALID: Choose a different type of chord (Triad, Bright Triad, Augmented, Diminished, Dominant 7th)?: ")

    # Connects the program to a MongoDB database where the data of the chords are stored as JSON documents
    cluster = "mongodb+srv://rajaesakimuthu997:kalVeeR*7681@clusterchords.mgjge.mongodb.net/?retryWrites=true&w=majority&appName=ClusterChords"
    client = MongoClient(cluster, tlsCAFile=certifi.where())
    db = client.store
    collection = db.chords

    # Makes a query and identifies which document's data is need according to the user's input on the type of chord they want
    doc = collection.find_one({"_id": f'{chord_type}'})

    # Prints out the data of chord they want for their tune according to the type of chord they chose and the scale of the tune
    for chords in doc[f'{song_scale}']:
        left_hand = chords['Left Hand'][0]
        right_hand = chords['Right Hand'][0]
        print("            LEFT HAND                RIGHT HAND")
        print()
        print(f'ORDER 1:    {left_hand["Order 1"]}         {right_hand["Order 1"]}')
        print(f'ORDER 2:    {left_hand["Order 2"]}         {right_hand["Order 2"]}')
        print(f'ORDER 3:    {left_hand["Order 3"]}         {right_hand["Order 3"]}')
        print(f'ORDER 4:    {left_hand["Order 4"]}         {right_hand["Order 4"]}')
        print(f'ORDER 5:    {left_hand["Order 5"]}         {right_hand["Order 5"]}')
    print() 

    # Asks if the user wants to try a different type of chord other than the one they chose, if yes, the program will rerun, if no, the program will end
    try_new_chord = input("Do you want to try a different type of chords? (Yes = Y, or No = N): ")

    if try_new_chord == "N":
        print()
        print("Thank You for using ChordFinder!!")

