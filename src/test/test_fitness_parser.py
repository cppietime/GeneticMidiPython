import genetic_music as gm

def test_parser():
    obj = [
        {"function": "silent", "bias": 0.5, "weight": 1},
        {"function": "new_notes", "bias": 0, "weight": 1},
        {"function": "repeated_precisely", "bias": 1, "weight": 2, "args": {"dist": 2}}
    ]
    notes = [-1, -2, 5, 4, 3, 4]
    fitness_func = gm.parse_fitness(obj)
    fitness = fitness_func(notes)
    expected_fitness = -1 * abs(2./6 - 0.5) + -1 * abs(4./6) + -2 * abs(1./2)
    assert abs(expected_fitness - fitness) < 1e-6, f'{fitness} does not match {expected_fitness}'

def main():
    test_parser()

if __name__ == '__main__':
    main()
