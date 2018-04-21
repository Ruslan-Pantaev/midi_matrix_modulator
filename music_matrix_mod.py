# Author:       Ruslan Pantaev
# Date:         2018-4-20
# Description:  Py2.7

# import pprint
from music21 import *

# ref http://web.mit.edu/music21/doc/moduleReference/moduleEnvironment.html
# music21.environment.UserSettings()['warnings'] = 0
# disabling py2 -> py3 msg
us = environment.UserSettings()
for key in sorted(us.keys()):
  key
us['warnings'] = 0

def print_midi_chart():
  print("\nOctave | C    | Db   | D    | Eb   | E    | F    | Gb   | G    | Ab   | A    | Bb   | B    ")
  oct_adder = 0

  for x in range (-1, 10):
    print("  %-*d" % (4, x)),
    for i in range(0, 12):
      midi_note = i + oct_adder
      if midi_note < 128:
        print("| %-*d " % (3, midi_note)),
    print("")
    oct_adder += 12

def get_note_name( midi_num ):
  note = ""
  if midi_num % 12 == 0:
    note += "C"
  elif midi_num % 12 == 1:
    note += "C#"
  elif midi_num % 12 == 2:
    note += "D"
  elif midi_num % 12 == 3:
    note += "D#"
  elif midi_num % 12 == 4:
    note += "E"
  elif midi_num % 12 == 5:
    note += "F"
  elif midi_num % 12 == 6:
    note += "F#"
  elif midi_num % 12 == 7:
    note += "G"
  elif midi_num % 12 == 8:
    note += "G#"
  elif midi_num % 12 == 9:
    note += "A"
  elif midi_num % 12 == 10:
    note += "A#"
  elif midi_num % 12 == 11:
    note += "B"

  if midi_num < 12:
    note += "-1"
  elif midi_num < 24:
    note += "0"
  elif midi_num < 36:
    note += "1"
  elif midi_num < 48:
    note += "2"
  elif midi_num < 60:
    note += "3"
  elif midi_num < 72:
    note += "4"
  elif midi_num < 84:
    note += "5"
  elif midi_num < 96:
    note += "6"
  elif midi_num < 108:
    note += "7"
  elif midi_num < 120:
    note += "8"
  else:
    note += "9"

  return note

def print_notes( arr ):
  for i in range(len(arr)):
    print("\n_________\nsection %d\n_________\n" % (i+1))
    for j in range(len(arr[i])):
      print("chord %d: " % (j+1)),
      for k in range(len(arr[i][j])):
        print("%-*s" % (4, get_note_name(arr[i][j][k]))),
      print("")

def transpose( chords ):
  print("Transposing Sets...")
  # ref https://www.geeksforgeeks.org/transpose-matrix-single-line-python/
  transposed_arr = [[chords[j][i] for j in range(len(chords))] for i in range(len(chords[0]))]
  for row in transposed_arr:
    print(row)
  return transposed_arr

def sum( arr ):
  print("Summing Sets...")
  sum_arr = [[0 for k in range(len(arr[0][0]))] for j in range(len(arr[0]))]
  oct_offset = 24
  for i in range(len(arr)):
    for j in range(len(arr[i])):
      # rows
      for k in range(len(arr[i][j])):
        sum_arr[j][k] += arr[i][j][k] - oct_offset
  return sum_arr # return single summed set

def subtract( arr ):
  print("Subtracting Sets...")
  subtr_arr = [[0 for k in range(len(arr[0][0]))] for j in range(len(arr[0]))]
  oct_offset = 60
  for i in range(len(arr)):
    # sections
    for j in range(len(arr[i])):
      # rows
      for k in range(len(arr[i][j])):
        if i == 0:
          # initing first set to later subtract from
          subtr_arr[j][k] = arr[0][j][k]
        else:
          subtr_arr[j][k] = abs(subtr_arr[j][k] - arr[i][j][k]) + oct_offset
  return subtr_arr # return single summed set

# TODO <3 write out complete custom chords and scales dictionary ;)
class chords_scales():
  dict = {
  'C': 'C4 E4 G4', 'C-': 'C4 D#4 G4'
  }

def main():
  # testing dict
  print(chords_scales.dict['C'])
  print(chords_scales.dict['C-'])

  sets_size = input("how many Sections? ")
  row_size = input("number of Chords? ")
  col_size = input("number of Voices per chord? ")

  # init 3d arr
  master_arr = [[[0 for k in range(col_size)] for j in range(row_size)] for i in range(sets_size)]
  # pprint.pprint(master_arr)

  print_midi_chart()

  print("\n(please refer to midi note chart above for reference)\n")

  for i in range(0, sets_size):
    for j in range(0, row_size):
      for k in range(0, col_size):
        master_arr[i][j][k] = input("note number %d of chord %d in section %d: " % (k+1, j+1, i+1))
        # s1.append(note.Note(get_note_name(master_arr[i][j][k]), type='quarter'))
        # s1.show('midi') # broken; quicktime doesn't handle midi files

  st = stream.Stream() # music21
  for i in range(0, sets_size):
    for j in range(0, row_size):
      st.append(chord.Chord(master_arr[i][j], type='half'))
  fp = st.write('midi', fp='./test_original.mid')

  print("")

  print("--------ORIGINAL start--------\n")
  for i in range(0, sets_size):
    print("original section %d" % (i + 1))
    for j in range(0, row_size):
      print(master_arr[i][j])

  print_notes(master_arr)
  print("\n--------ORIGINAL end----------\n")

  print("--------TRANSPOSED start------\n")
  transposed_arr = []
  for i in range(0, sets_size):
    transposed_arr.append(transpose(master_arr[i]))

  st = stream.Stream() # resetting Stream
  # d = duration.quarterConversion(2.0/3.0).tuplet
  d = duration.Duration(8.0 / 6.0) # 8 quarterNotes divided by 6 (halfNote triplets)
  for i in range(len(transposed_arr)):
    for j in range(len(transposed_arr[i])):
      # ch = chord.Chord(transposed_arr[i][j]).closedPosition()
      st.append(chord.Chord(transposed_arr[i][j], duration=d).closedPosition())
  fp = st.write('midi', fp='./test_transposed.mid')

  print_notes(transposed_arr)
  print("\n--------TRANSPOSED end--------\n")

  print("--------SUMMING start---------\n")
  st = stream.Stream()
  sum_arr = sum(master_arr)
  # printing
  for i in range(len(sum_arr)):
    for j in range(len(sum_arr[i])):
      print("%-*s" % (4, get_note_name(sum_arr[i][j]))),
    print("")
  # streaming
  for i in range(len(sum_arr)):
    st.append(chord.Chord(sum_arr[i], type='half').closedPosition())
  fp = st.write('midi', fp='./test_summed.mid')
  print("\n--------SUMMING end-----------\n")

  print("--------SUBTRACTING start-----\n")
  st = stream.Stream()
  subtr_arr = subtract(master_arr)
  # printing
  for i in range(len(subtr_arr)):
    for j in range(len(subtr_arr[i])):
      print("%-*s" % (4, get_note_name(subtr_arr[i][j]))),
    print("")
  # streaming
  for i in range(len(subtr_arr)):
    st.append(chord.Chord(subtr_arr[i], type='half').closedPosition())
  fp = st.write('midi', fp='./test_subtracted.mid')
  print("\n--------SUBTRACTING end-------\n")

  # TODO set1 x set1 | set2 x set2 | ... | setn x setn

  # TODO set1 x set2 | set1 x set3 | ... | (every combination of pairs of sets)

if __name__ == '__main__':
  main()
