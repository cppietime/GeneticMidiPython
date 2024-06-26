import collections

from .typedefs import *

def fraction_silent(mus: Music) -> float:
    """Fraction of time in mus that is silent."""
    last_note = None
    silence = 0
    for note in mus:
        if note == -1 or (note == -2 and last_note == None):
            silence += 1
        if note == -1:
            last_note = None
        elif note != -2:
            last_note = note
    return silence / len(mus)

def fraction_new_notes(mus: Music) -> float:
    """Fraction of timestamps that are note-on."""
    new = 0
    for note in mus:
        if note >= 0:
            new += 1
    return new / len(mus)

def fraction_repeated_notes(mus: Music, dist:int=4) -> float:
    """Fraction of notes-on that are the same pitch as a previous note-on."""
    recent_notes = {}
    queue = collections.deque()
    score = 0
    num_notes = 0
    for note in mus:
        if note < 0:
            continue
        num_notes += 1
        if recent_notes.get(note, 0) > 0:
            score += 1
        if len(queue) >= dist:
            last_note = queue.popleft()
            recent_notes[last_note] -= 1
        queue.append(note)
        recent_notes[note] = recent_notes.get(note, 0) + 1
    return score / num_notes if num_notes else 0

def fraction_repeated_precisely(mus: Music, dist: int=4) -> float:
    """Fraction of notes that are identical to that from a previous time."""
    if len(mus) <= dist:
        return 0
    score = 0
    divisor = 0
    for i, note in enumerate(mus[:-dist]):
        if note < 0:
            continue
        divisor += 1
        if note == mus[i + dist]:
            score += 1
    return score / divisor if divisor else 0

def note_mean(mus: Music) -> float:
    """Mean of note pitches."""
    filtered = [x for x in mus if x >= 0]
    return sum(filtered) / len(filtered) if filtered else 0

# Would standard deviation be more useful?
def note_variance(mus: Music) -> float:
    """Variance of note pitches."""
    notes = [note for note in mus if note >= 0]
    if not notes:
        return 0
    mean = sum(notes) / len(notes)
    return sum([(note - mean) ** 2 for note in notes]) / len(notes) if notes else 0

_default_intervals = {
    0: 0.5,
    1: 0,
    2: 0.2,
    3: 0.2,
    4: 0.5,
    5: 0.4,
    6: 0.4,
    7: 1,
    8: 0.5,
    9: 0.2,
    10: 0.2,
    11: 0
}
def consecutive_intervals(mus: Music, intervals:dict[int, float]=_default_intervals) -> float:
    """Score of intervals between consecutive notes. Resets on rest."""
    last_note = None
    changes = 0
    score = 0
    for note in mus:
        if note == -1:
            last_note = None
            continue
        if note >= 0:
            if last_note != None:
                changes += 1
                interval = (note - last_note) % 12
                score += intervals[interval]
            last_note = note
    return score / changes if changes else 0

def _bit_reverse(i: int, width: int) -> int:
    bstr = f'{i:0{width}b}'
    return int(bstr[::-1], 2)

def _syncopation_score(timestamp: int, modulus: int) -> float:
    timestamp %= modulus
    width = (modulus - 1).bit_length()
    rev = _bit_reverse(timestamp, width)
    return rev.bit_length()

def syncopation(mus: Music, modulus:int=0) -> float:
    """Score of syncopation. Higher score is more syncopated."""
    if modulus <= 0:
        modulus = len(mus)
    score = 0
    divisor = 0
    for i, note in enumerate(mus):
        sync_score = _syncopation_score(i, modulus)
        divisor += sync_score
        if note >= 0:
            score += sync_score
    return score / divisor if divisor > 0 else 0

def fraction_in_scale(mus: Music, scale: set[int]) -> float:
    """Fraction of notes that are in the provided scale modulo 12."""
    current_note = None
    score = 0
    notes = 0
    for note in mus:
        if note >= 0:
            current_note = note
        elif note == -1:
            current_note = None
        if current_note != None:
            notes += 1
            if current_note % 12 in scale:
                score += 1
    return score / notes if notes > 0 else 0

def _note_lengths(mus: Music) -> list[int]:
    length = 0
    last_note = None
    lengths = []
    def note_end():
        nonlocal last_note, length, lengths
        if last_note != None and length > 0:
            lengths.append(length)
        length = 0
    for note in mus:
        if note != -2:
            # Not a continuing note
            note_end()
            last_note = None if note == -1 else note
        length += 1
    note_end()
    return lengths

def length_mean(mus: Music) -> float:
    """Mean length of held notes."""
    lengths = _note_lengths(mus)
    return sum(lengths) / len(lengths) if lengths else 0

def length_variance(mus: Music) -> float:
    """Variance in length of held notes."""
    lengths = _note_lengths(mus)
    if not lengths:
        return 0
    mean = sum(lengths) / len(lengths)
    return sum([(x - mean) ** 2 for x in lengths]) / len(lengths)
    
