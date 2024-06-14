import time

import music

def main():
    scale = [(60 + x) % 12 for x in [0, 2, 4, 5, 7, 9, 11]]
    chromatic = range(60, 72)
    population = [music.random_sequence(12, chromatic) for _ in range(100)]
    fitness_func = lambda pop: -abs(music.fraction_silent(pop) - 0.125) + -abs(music.fraction_new_notes(pop) - 1) + -abs(music.fraction_repeated_precisely(pop, 5) - 0.75) + -abs(music.consecutive_intervals(pop) - 0.5) - abs(music.fraction_in_scale(pop, scale) - 1) * 0.25
    choice = population[-1]
    print(f'Initial fitness = {fitness_func(choice)}')
    print(f'Scale amt = {music.fraction_in_scale(choice, scale)}')
    for i in range(4):
        for _ in range(20):
            population = music.generation(population, fitness_func, scale=chromatic)
        choice = population[-1]
        print(f'Fitness #{i} = {fitness_func(choice)}')
        print(f'Scale amt = {music.fraction_in_scale(choice, scale)}')
        music.play_sequence(choice)
        time.sleep(1)

def test_len():
    print(music._note_lengths([1]))
    print(music._note_lengths([-1]))
    print(music._note_lengths([1, 2, 3, 4]))
    print(music._note_lengths([1, -2, -2, -2]))
    print(music._note_lengths([-1, -2, -2, -2]))
    print(music._note_lengths([-1, -2, 4, -2]))
    print(music._note_lengths([-1, -2, 4, 5]))

if __name__ == '__main__':
    test_len()
