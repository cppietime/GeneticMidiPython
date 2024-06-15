import random
import time

import mido

from .typedefs import *

def uniform_note(scale=None) -> int:
    """Generate a single random note from the provided scale.
    If a scale is not provided, choose from all valid MIDI notes [0-127].
    There is a 1/6 chance for a rest and a 1/6 chance for a note continuation.
    """
    cls = random.randint(0, 5)
    if cls == 0:
        return -2
    if cls == 1:
        return -1
    scale = scale or range(128)
    return random.choice(scale)

def random_sequence(length: int, scale=None) -> Music:
    """Produce a random sequence of notes of a specific length."""
    return [uniform_note(scale) for _ in range(length)]

def play_sequence(notes: Music, timescale:float=1./4):
    """Play a sequence using MIDO's default backend."""
    with mido.open_output() as output:
        last_note = None
        for note in notes:
            if note != -2 and last_note != None:
                output.send(mido.Message('note_off', note=last_note))
            if note >= 0:
                last_note = note
                output.send(mido.Message('note_on', note=note, velocity=63))
            elif note == -1:
                last_note = None
            time.sleep(timescale)
        if last_note is not None:
            output.send(mido.Message('note_off', note=last_note))

def mutate(notes: Music, chance:float=1./8, scale=None) -> Music:
    """Randomly change all notes with a provided chance."""
    notes = list(notes)
    for i, _ in enumerate(notes):
        if random.random() <= chance:
            notes[i] = uniform_note(scale)
    return notes

def crossover(left: Music, right: Music) -> Music:
    """Crossover two musical pieces by randomly selecting from each."""
    # TODO allow crossover between arbitrary numbers of parents
    assert len(left) == len(right), "Parent lengths do not match"
    child = [left[i] if random.random() < 0.5 else right[i] for i in range(len(left))]
    return child

def generation(population: Population, fitness_func, mutation_chance=1./8, mutation_fraction=0.25, crossover_fraction=0.25, scale=None) -> Population:
    """Process a single generation."""
    # Shuffle
    random.shuffle(population)
    # Mutate
    upto = int(len(population) * mutation_fraction)
    for i in range(upto):
        population[i] = mutate(population[i], mutation_chance, scale)
    # Evaluate fitness
    fitness = [(mus, fitness_func(mus)) for mus in population]
    # Sort by fitness
    fitness = sorted(fitness, key=lambda x: x[1])
    # Crossover
    upto = int(len(population) * crossover_fraction)
    for i in range(upto):
        left = random.choice(fitness[upto:])[0]
        right = random.choice(fitness[upto:])[0]
        fitness[i] = (crossover(left, right), 0)
    return [f[0] for f in fitness]
