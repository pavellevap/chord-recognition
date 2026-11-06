# Fretboard Chord Drill

A single-page drill: a chord is shown in standard notation (treble clef, guitar octave),
and you find its exact pitches on a 19-fret guitar neck.

- `index.html` is the whole app. It is published as a claude.ai Artifact
  (https://claude.ai/artifact/ToKamrzMfJwgTyassn84N8), which wraps it in a document skeleton.
- Notation is drawn with VexFlow 4.2.5 (loaded from jsDelivr).
- Run history is stored per user in the Artifact's `db` store (`data/users/<id>/…`),
  with `localStorage` as a fallback when the store is unavailable.

## How it works

- **Settings** (modelled on musictheory.net's chord exercise): chords per run, key signatures
  (one picked at random per run), major/minor/both, chord types, inversions, written-pitch range,
  chord notes (key + neighbours / key only / any), guitar voicings (with max stretch and doubled notes), double accidentals, sound.
- **Chord notes**: with "key + neighbours" every note of a chord comes from the run's key signature
  or one a sharp/flat away (in C: C, F or G major); chords taken from a neighbour are labelled
  "from F major" etc. after you solve them. A fully diminished 7th only needs three of its four
  notes in the key (B D F A♭ in C major).
- **Guitar voicings** are found by searching the neck: one note per string, every chord tone present,
  all positions (open strings count as fret 0) within the max stretch. With doubled notes on,
  shapes may repeat chord tones on adjacent strings and must fit four fingers (a barre counts as one).
  With voicings off, chords are close-position stacks as on musictheory.net.
- **Before each run** a fretboard shows scale degrees 1–7 for the run's key; 1, 3 and 5 are colored.
- **During a run** you tap notes and press Check. Wrong notes turn red and you retry until correct;
  accuracy counts chords solved on the first try without "Show answer".
- **History** keeps one entry per distinct setup with run count, last run, and decaying averages of
  score and time (each new run weighted 10%, bias-corrected so early averages are not skewed).
