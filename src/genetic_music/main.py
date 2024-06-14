import time

from . import music

def main():
    scale = [(60 + x) % 12 for x in [0, 2, 4, 5, 7, 9, 11]]
    chromatic = range(60, 60+12*2)
    population = [music.random_sequence(32, chromatic) for _ in range(100)]
    fitness_func = lambda pop: -abs(music.fraction_silent(pop) - 0) + -abs(music.fraction_new_notes(pop) - 0.75) + -abs(music.fraction_repeated_precisely(pop, 4) - 0.5) * 40 + -abs(music.consecutive_intervals(pop) - 0.33) - abs(music.fraction_in_scale(pop, scale) - 1) * 5 - abs(music.syncopation(pop) - 1) - abs(music.fraction_repeated_notes(pop, 1) - 0) - abs(music.length_mean(pop) - 1.25) - abs(music.length_variance(pop) - 1)
    choice = population[-1]
    print(f'Initial fitness = {fitness_func(choice)}')
    for i in range(4):
        for _ in range(200):
            population = music.generation(population, fitness_func, scale=chromatic)
        choice = population[-1]
        print(f'Fitness #{i} = {fitness_func(choice)}')
        music.play_sequence(choice)
        time.sleep(1)

if __name__ == '__main__':
    main()
