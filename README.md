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
  roots any/in key, one note per string, double accidentals, sound.
- **Before each run** a fretboard shows scale degrees 1–7 for the run's key; 1, 3 and 5 are colored.
- **During a run** you tap notes and press Check. Wrong notes turn red and you retry until correct;
  accuracy counts chords solved on the first try without "Show answer".
- **History** keeps one entry per distinct setup with run count, last run, and decaying averages of
  score and time (each new run weighted 10%, bias-corrected so early averages are not skewed).
