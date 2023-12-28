# all_scales.py

'''
This program takes a string as input and prints the name(s) of the scale.
The string is matched against the first column of the CSV file.
If the string exists, the text in the second column is printed.
If the string does not exist, a message is printed.

The CSV file is a list of scales and their names.
The first column contains the scale as a string, using the
semitone count ascending from the first note.
For example, the major scale is represented as '2212221'.
The second column contains the name of the scale.

The CSV file is read into a Pandas DataFrame.
The first column is converted to strings.
The user is asked to input a string of the semitones.
The string is matched against the first column of the DataFrame.


'''
import pandas as pd
import streamlit as st
import numpy as np
import io
from pydub import AudioSegment
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"


# Hide the menu and github logo from being displayed
# when others are viewing the page
hide_github_icon = """<style> .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }</style>"""

st.markdown(hide_github_icon, unsafe_allow_html=True)



# Load the CSV file and read the first column as strings
df = pd.read_csv('all_scales.csv', header=None, dtype={0: str})

# Frequency of middle C in Hz
START_PITCH= 440.0

# Sampling rate, or number of measurements per second
SAMPLE_RATE = 44100

NOTE_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']




# CSS to change the color of the button
# Use custom CSS to Streamlit widgets using the st.markdown function with 
# the unsafe_allow_html=True parameter. In this example, the CSS changes the background color 
# of ALL buttons to #0099ff and the text color to #ffffff. 
# When you hover over a button, the background color changes to #00ff00 and the text color to #ff0000. 
# You can replace these color codes with the colors you want.

#Please note that using unsafe_allow_html=True could have security implications 
# if you’re not in control of the HTML input. In this case, since you’re generating 
# the HTML yourself, it should be safe.

st.markdown("""
    <style>
        div.stButton > button:first-child {
            background-color: #66CCCC;
            color: #000000;
        }
        div.stButton > button:hover {
            background-color: #339999;
            color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
    <style>
        body {
            color: #000000;
        }
    </style>
    """, unsafe_allow_html=True)




# -------------- ORIG FUNCTIONS USING SIMPLEAUDIO LIBRARY --------------------------------

# Function to generate a sine wave of a specific frequency
# def generate_sine_wave(freq, duration, sample_rate=44100, amplitude=0.3, fade_duration=0.01):
#     t = np.linspace(0, duration, int(sample_rate * duration), False)
#     note = amplitude * np.sin(freq * t * 2 * np.pi)
#     # Apply fade-in and fade-out
#     fade_samples = int(fade_duration * sample_rate)
#     fade_in = np.linspace(0, 1, fade_samples)
#     fade_out = np.linspace(1, 0, fade_samples)
#     note[:fade_samples] *= fade_in
#     note[-fade_samples:] *= fade_out
#     return (note * 32767).astype(np.int16)





# Function to play a sequence of notes
# def play_notes(sequence, duration, root_freq, sample_rate=SAMPLE_RATE):
#     # Frequencies of notes in a chromatic scale up to two octaves
#     chromatic_scale = [root_freq * 2**(n/12) for n in range(25)]  # 25 notes for two octaves
#     current_note = 0  # Start at the root note
#     # Play the root note
#     note = generate_sine_wave(chromatic_scale[current_note], duration, sample_rate)
#     play_obj = sa.play_buffer(note, 1, 2, sample_rate)
#     play_obj.wait_done()
#     # Generate and play each note in the sequence
#     for step in sequence:
#         current_note += int(step)
#         freq = chromatic_scale[current_note % len(chromatic_scale)]
#         note = generate_sine_wave(freq, duration, sample_rate)
#         play_obj = sa.play_buffer(note, 1, 2, sample_rate)
#         play_obj.wait_done()
#     # Reverse the sequence and the direction of each step for the descent
#     for step in reversed(sequence):
#         current_note -= int(step)
#         freq = chromatic_scale[current_note % len(chromatic_scale)]
#         note = generate_sine_wave(freq, duration, sample_rate)
#         play_obj = sa.play_buffer(note, 1, 2, sample_rate)
#         play_obj.wait_done()


# --------------------------------------------------------------------------------------------
        








# -------------- REPLACEMENT FUNCTIONS USING PYAUDIO LIBRARY --------------------------------

import pyaudio
import numpy as np

# Function to generate a sine wave of a specific frequency
def generate_sine_wave(freq, duration, sample_rate=44100, amplitude=0.3, fade_duration=0.01):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note = amplitude * np.sin(freq * t * 2 * np.pi)
    # Apply fade-in and fade-out
    fade_samples = int(fade_duration * sample_rate)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    note[:fade_samples] *= fade_in
    note[-fade_samples:] *= fade_out
    return (note * 32767).astype(np.int16)




# ----------------------- PYAUDIO version of play_notes - this also failed to work -----------------
# Function to play a sequence of notes
# def play_notes(sequence, duration, root_freq, sample_rate=44100):
#     p = pyaudio.PyAudio()
#     stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)
#     # Frequencies of notes in a chromatic scale up to two octaves
#     chromatic_scale = [root_freq * 2**(n/12) for n in range(25)]  # 25 notes for two octaves
#     current_note = 0  # Start at the root note
#     # Play the root note
#     note = generate_sine_wave(chromatic_scale[current_note], duration, sample_rate)
#     stream.write(note.tobytes())
#     # Generate and play each note in the sequence
#     for step in sequence:
#         current_note += int(step)
#         freq = chromatic_scale[current_note % len(chromatic_scale)]
#         note = generate_sine_wave(freq, duration, sample_rate)
#         stream.write(note.tobytes())
#     # Reverse the sequence and the direction of each step for the descent
#     for step in reversed(sequence):
#         current_note -= int(step)
#         freq = chromatic_scale[current_note % len(chromatic_scale)]
#         note = generate_sine_wave(freq, duration, sample_rate)
#         stream.write(note.tobytes())
#     stream.stop_stream()
#     stream.close()
#     p.terminate()


# -----------------------------------------------------------------------------------------








# --------------- play_audio version using pydub and io

# In this version, we generate the audio data in the server environment and then send it
# to the client’s web browser to be played.
# Correct, when you use the st.audio function to play audio data in Streamlit, 
# the audio data is sent to the client’s web browser and played there. No audio files 
# are downloaded to the user’s computer. The audio data is streamed from the server 
# and played in the browser, and it does not remain on the user’s computer after the page is closed. 
# This makes it a good solution for playing audio in a web app without needing to download 
# any files to the user’s computer.


def play_notes(sequence, duration, root_freq, sample_rate=44100):
    # Frequencies of notes in a chromatic scale up to two octaves
    chromatic_scale = [root_freq * 2**(n/12) for n in range(25)]  # 25 notes for two octaves
    current_note = 0  # Start at the root note
    # Play the root note
    note = generate_sine_wave(chromatic_scale[current_note], duration, sample_rate)
    notes = note.tobytes()
    # Generate each note in the sequence
    for step in sequence:
        current_note += int(step)
        freq = chromatic_scale[current_note % len(chromatic_scale)]
        note = generate_sine_wave(freq, duration, sample_rate)
        notes += note.tobytes()
    # Reverse the sequence and the direction of each step for the descent
    for step in reversed(sequence):
        current_note -= int(step)
        freq = chromatic_scale[current_note % len(chromatic_scale)]
        note = generate_sine_wave(freq, duration, sample_rate)
        notes += note.tobytes()
    # Convert raw data to WAV
    audio_segment = AudioSegment(notes, frame_rate=sample_rate, sample_width=2, channels=1)
    # Convert WAV to WAV
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    return wav_io.getvalue()


# -------------------------------------------------------------------------------------------------
















# Function to generate all possible scales with n intervals and k semitones
def generate_scales(n, k, scale=''):
    """
    Generates all possible scales with n intervals and k semitones.

    Parameters:
    - n: The number of intervals in the scale
    - k: The total number of semitones in the scale
    - scale: The current scale being generated (default: '')

    Returns:
    - A list of all generated scales
    """
    scales = []  # Initialize an empty list to store the scales

    # Base case: if n is 0 and k is 0, add the scale to the list
    if n == 0 and k == 0:
        scales.append(scale)
    # Recursive case: if n is positive and k is positive, generate scales with 1, 2, 3, or 4 semitones
    elif n > 0 and k > 0:
        for i in range(1, min(k, 9) + 1):
            scales.extend(generate_scales(n - 1, k - i, scale + str(i)))

    return scales




# Function to translate the numeric interval string into note names
def get_note_names(scale, starting_note):
    """
    Translates the numeric interval string into note names.

    Parameters:
    - scale: The numeric interval string representing the scale
    - starting_note: The starting note of the scale

    Returns:
    - A string representing the scale with note names
    """
    scale_string = ''

    try:
        note_index = NOTE_NAMES.index(starting_note)
    except ValueError:
        note_index = 0  # Default to C if starting_note is not found

    cur_degree = note_index
    scale_string += NOTE_NAMES[cur_degree] + ' '

    for interval in scale:
        cur_degree = (cur_degree + int(interval)) % 12
        scale_string += NOTE_NAMES[cur_degree] + '  '

    return scale_string


 
 
 


# ------------- SIDEBAR CONTENT------------------------------------------------------------------
# Add a header to the sidebar
st.sidebar.header('Overview')

# Add text to the sidebar
# Note: to add superscripts to markdown, you have to use Unicode characters:
# ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁰
# You can enter these as: \u00b9 \u00b2 \u00b3 \u2074 \u2075 \u2076 \u2077 \u2078 \u2079 \u2070
# Or you can copy and paste them from here: https://www.compart.com/en/unicode/superscript
st.sidebar.markdown('This utility gives you access to 1,981 possible scales. All of these have between 4 and 12 semitones\u00b9, notes are spaced from 1–9 semitones, and the total number of semitones is 12 (one octave).')
st.sidebar.markdown('*Ex: 13161 is a valid 1-octave scale. The sum of the digits is 12, and each digit is between 1–9. The scale is: C Db E F B C.*')
st.sidebar.markdown('Approximately 20% of these scales have one or more names, which will be shown.')
st.sidebar.markdown('This is a great way to hear new scales for a fresh sound in your compositions. You can make up any combination of intervals that fit within an octave. When you find a scale you like, simply copy the semitone pattern to translate into any key.')
st.sidebar.markdown('*Ex: If you like a combination such as 141321 and want to start on D, it would be D Eb G Ab B Db D*')

st.sidebar.markdown('---')

# created bulleted list for the 3 sections
st.sidebar.markdown('There are 3 search methods:')
# List items
sections = ['By semitone definition', 'By scale name', 'By interval count']
# Convert list to markdown
sections_md = "\n".join(f"- {item}" for item in sections)
# Display in sidebar
st.sidebar.markdown(sections_md)

st.sidebar.markdown('---')

st.sidebar.markdown('With regards to semantics, the number of notes in a scale does not include the note an octave above the root. For example, a major scale has 7 notes, not 8. In this utility, the number of intervals is the same as the number of notes because the final interval gets you to an octave above the root.')

st.sidebar.markdown('*Ex: The C major scale: C D E F G A B C has 7 intervals from C to C, and we refer to this as a 7-note scale (technically from C to B).*')



# Add a graphic to the sidebar
st.sidebar.image('robot_keyboard.png')

st.sidebar.markdown('---')

# Add a subheader to the sidebar
st.sidebar.header('How to use')

st.sidebar.markdown('Each section has instructions and should be easy to use. Note that 403 of the scales have names taken from a variety of sources, including Western classical music, jazz, popular, Indian classical music, and others.')

st.sidebar.markdown('Many scales have more than one name, depending on the origin and/or primary use of the scale. For example, a traditional major scale has 18 other names!')

st.sidebar.markdown('In the first section, every time you enter a semitone pattern (such as 123114), be sure that the sum of the digits equals 12, then press the **Get scale names** button.')

st.sidebar.markdown('Also, if you are using the second or third section (which will give you the semitone patterns of various scales), you can copy/paste the pattern into the top section to hear it.')

st.sidebar.markdown('---')

# Add a subheader to the sidebar
st.sidebar.header('How many scales?')

st.sidebar.markdown('There are 1,981 possible scales having 4–12 intervals\u00b9 that span one octave. All of these are in my database, and they will appear if you type the semitone pattern in the top search bar. For example, if you type 212412, you will see the four names of this scale are: *Raga Bagesri, Sriranjani, Kapijingla, and Jayamanohari.*')

st.sidebar.markdown("\u00b9 I don't allow 1-, 2-, or 3-interval scales because they are rarely used (and generally not even considered scales). For example, a 'scale' with 3 intervals, such as 435, is simply an arpeggiated major chord.")

st.sidebar.markdown('---')

st.sidebar.markdown("***Find an error or omission?*** Please let me know if you find any scales that are missing names, and I'll add them to the database.*")

st.sidebar.markdown('*Thank you for looking at this utility. In addition to its research value, I hope it will be useful for you to explore new scales to use in your compositions.*')


st.sidebar.markdown(' ')
   
# Add a graphic to the sidebar
st.sidebar.image('keyboard_cat.png')



# Add a header to the sidebar
#st.sidebar.header('This is a header in the sidebar.')

# Add a subheader to the sidebar
#st.sidebar.subheader('This is a subheader in the sidebar.')







# ------------- MAIN PAGE CONTENT------------------------------------------------------------------

# Display the image at the top of the main page
st.image('piano_keyboard.png')


# Set the title of the app
st.title('Octave scales with 4–12 notes')
st.subheader('Total possible scales: 1,981')
# NOTE: st.title() should be called only once in your app because it’s intended 
# to be used for the main title of your app. If you need to use headers in other parts of your app,
# consider using st.header(), st.subheader(), or st.markdown() with appropriate markdown syntax.


# Display your email address
st.markdown('by [David Collett](mailto:tangled.rhythms@gmail.com),       *GNU General Public License v3.0*')


# Load the CSV file and read the first column as strings
#df = pd.read_csv('all_scales.csv', header=None, dtype={0: str})







# --------- SECTION 1: SEMITONE DEFINITION -------------------------------------------------

st.write('---')

# Header for the semitone definition entry section
st.header('Semitone definition entry (single scale)')


# Ask the user to input a string
user_input = st.text_input('To find the name(s) of a scale, enter 4–12 single digits whose sum is 12, no spaces. These represent the semitones between notes, starting at the root note (for example, 2212221 is a major scale).', key='user_input')

# Remove spaces from the user input
note_sequence = user_input.replace(' ', '')


# Initialize num_octaves to 1 (user may change to 2 if playback = On)
num_octaves = 1
# Initialize note_duration = 0.5 (user may change from 0.25 to 1.0 if playback = On)
note_duration = 0.25


# user can select whether to playback the sound or not
playback = st.radio(
    'Playback:', ('Off', 'On'), key='playback_key')

# if playback = On, then the user can select 1 or 2 octaves for playback
if playback == 'On':
    num_octaves = st.radio(
        'Select 1 or 2 octaves for playback:', (1, 2), key='octave_key')

    # Choose the note duration
    note_duration_options = [0.0625, 0.125, 0.25, 0.33, 0.5, 0.66, 0.75, 1.0]
    note_duration = st.select_slider("Select the duration of each note (in seconds)",
                                     options=note_duration_options,
                                     value=0.25,
                                     key='note_duration_key'
                                     )


# initialize the current scale
cur_scale = ''

if playback == 'On':
    
    # Add a button for the user to click after entering their input
    button1 = st.button('Get scale names (if any) and PLAY scale', key='button_key1')

else:
    button1 = st.button('Get scale names (if any)', key='button_key1')
    
    
if button1:
    if note_sequence.isdigit():
        
        # Check if the sum of the digits is 12
        if (sum(int(digit) for digit in note_sequence) == 12) \
            and (4 <= len(note_sequence) <= 12):
                
            # Find the string in the first column
            row = df[df[0] == note_sequence]
                       
            if not row.empty:
                # If the string exists, print the text in the second column
                if pd.isnull(row.iloc[0, 1]):
                    st.write('This scale is unnamed.')
                    cur_scale = row.iloc[0, 0]
                else:
                    st.write(row.iloc[0, 1])
                    cur_scale = row.iloc[0, 0]

                if playback == 'On':
                    if num_octaves == 1:
                        scale_to_play = cur_scale
                        start_pitch = START_PITCH
                    elif num_octaves == 2:
                        scale_to_play = cur_scale + cur_scale
                        start_pitch = START_PITCH / 2
                        
                    # This was the "old" method using simpleaudio and pyaudio (which didn't work)
                    # play_notes(scale_to_play, note_duration, start_pitch)
                        
                    # This is the new method to try, using pydub and io
                    audio_data = play_notes(scale_to_play, note_duration, start_pitch)
                    st.audio(audio_data, format='audio/wav')

                   
            else:
                st.write('The string does not exist in the data.')
        else:
            st.write('Error: There must be 4–12 digits whose sum is 12. Please try again.')
    else:
        st.write('Error: There must be 4–12 digits whose sum is 12. Please try again.')

  
   
st.write('---')
  
  
  
  
  
  


# --------- SECTION 2: SCALE NAME SEARCH -------------------------------------------------    

# Header for the semitone definition entry section
st.header('Scale name search')
st.write('Enter a string to search for a scale name. For example, enter "major" to find all scales with "major" in the name. The search is case-insensitive. If the name is part of any scale name, the semitone pattern and scale name(s) will be displayed.')

# Create an empty DataFrame
df = pd.read_csv('all_scales.csv', header=None, dtype={0: str})

# Initialize search_string to ''
search_string = ''

# Search the database for any matches to a scale name
# Input string from user
search_string = st.text_input("Enter a string (and press RETURN):")

if search_string:
    
    # Convert the search string and DataFrame column to lowercase
    search_string = search_string.lower()
    df[1] = df[1].str.lower()

    # Search the DataFrame
    matched_rows = df[df[1].str.contains(search_string, na=False)]

    # Print the matched rows in the specified format
    for index, row in matched_rows.iterrows():
        st.write(f"{row[0]}: {row[1]}")

    # Print the total number of matches
    st.write(f'Total number of matches: {len(matched_rows)}')
    
    

     
st.write('---') 
    
    
 
    
    
    
 
 # ----- SECTION 3: FIND SCALES WITH n INTERVALS STARTING ON CERTAIN NOTE  ---------------------- 

# Header for the semitone definition entry section
st.header('Scales based on interval count')
st.write('Enter the number of intervals in the scale and the starting note. The table will display all scales containing this number of intervals: semitone pattern, name(s), and the note names of the scale starting on your chosen note.')

# Initialize an empty list to store the scales
#scales = []

# Call the function by setting n = total # intervals in a scale
# and k = total sum of all semitones.

# For example, a pentatonic scale (5 note scale, 5 intervals) within an octave,
# would have n = 5 and k = 12.

k = 12      # total # of semitones in an octave

# Define the options for the slider
num_intervals_options = list(range(4, 13))  # a list of integers from 4 to 12 inclusive

# Enter the number of intervals  (the last interval gets you back to the root an octave higher)
n = st.select_slider('Enter the number of intervals in the scale: ', num_intervals_options, key='num_intervals_key')

# Define the options for the slider
start_note_options = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# Create the select slider
starting_note = st.select_slider("Select the scale's starting note", NOTE_NAMES, key='starting_note_key')

# Generate the scales with n intervals and k semitones
scales = generate_scales(n, k)


# Set the starting note
if starting_note not in NOTE_NAMES:
    st.write(f'\n\n>>>>> {starting_note} is not a valid note name: Defaulting to C <<<<<')
    starting_note = 'C' 





# Header for the resulting semitone patterns, note names, scale name(s)
#st.header('Semitone patterns, note names, scale name(s)')

# Print the total number of scales and the scales themselves
st.write(f'List of all {n}-note ({n}-interval) octave scales where each interval is 1–9 semitones apart. These scales are a subset of the 1,981 scales in the database.')

st.write(f'\nTotal number of all such scales: {len(scales)}\n')






# Create an empty DataFrame
df_output = pd.DataFrame(columns=['Semitones', 'Note Names', 'Scale Name'])


for i, scale in enumerate(scales, 1):
    
    # See if the scale is in the database of scales
    # Find the string in the first column
    row = df[df[0] == scale]
    if not row.empty:
        # If the scale semitone patter exists, print the text in the second column (if any)
        if pd.isnull(row.iloc[0, 1]):
            scale_name = ' ' # no name for this scale
        else:
            scale_name = row.iloc[0, 1]
    
    # Append each output to the DataFrame
    df_output.loc[i] = [scale, get_note_names(scale, starting_note), scale_name]
    if i % 5 == 0:
        df_output.loc[i+1] = ['', '', '']



# Convert the DataFrame to a HTML table with custom column widths
# This was necessary in order to have the output neatly lined up.

# I have 3 columns, so above I had to define df_output with 3 titles.

html_table = df_output.to_html(index=False)

html_table = html_table.replace('<table border="1" class="dataframe">', '<table style="width:100%;">')

html_table = html_table.replace('<th>Scale</th>', '<th style="width:15%; text-align:center;">Scale</th>')

html_table = html_table.replace('<th>Note Names</th>', '<th style="width:40%; text-align:center;">Note Names</th>')

html_table = html_table.replace('<th>Scale Name</th>', '<th style="width:45%; text-align:center;">Scale Name</th>')

# Display the HTML table
st.markdown(html_table, unsafe_allow_html=True)


# Display the image
st.write(' ')
st.image('robot_piano.png')
