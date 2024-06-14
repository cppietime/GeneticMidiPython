import genetic_music as gm

# Test every fitness function

def assert_fraction(value: float, expected: float, epsilon:float=1e-6):
    diff = abs(value - expected)
    assert diff <= epsilon, f'{value=} did not match {expected=}'

def test_fraction_silent():
    assert_fraction(gm.fraction_silent([1]), 0)
    assert_fraction(gm.fraction_silent([1, 2, 3, 4]), 0)
    assert_fraction(gm.fraction_silent([-1]), 1)
    assert_fraction(gm.fraction_silent([-1, -1, -1, -1]), 1)
    assert_fraction(gm.fraction_silent([-1, -2]), 1)
    assert_fraction(gm.fraction_silent([-1, -2, -2, -1]), 1)
    assert_fraction(gm.fraction_silent([-1, -2, 4, 5]), .5)
    assert_fraction(gm.fraction_silent([-1, -2, 4, -2]), .5)
    assert_fraction(gm.fraction_silent([-1, -2, 4, -1]), .75)
    assert_fraction(gm.fraction_silent([1, -2, 3, -2]), 0)
    assert_fraction(gm.fraction_silent([1, -2, -1, -1]), 0.5)
    assert_fraction(gm.fraction_silent([1, -2, -1, -2]), 0.5)

def test_fraction_new_notes():
    assert_fraction(gm.fraction_new_notes([1]), 1)
    assert_fraction(gm.fraction_new_notes([1, 2, 3, 4]), 1)
    assert_fraction(gm.fraction_new_notes([-1]), 0)
    assert_fraction(gm.fraction_new_notes([-1, -1]), 0)
    assert_fraction(gm.fraction_new_notes([-1, -2]), 0)
    assert_fraction(gm.fraction_new_notes([1, -2]), 0.5)
    assert_fraction(gm.fraction_new_notes([1, -2, -2, -1, -2, -1]), 1./6)

def test_fraction_repeated_notes():
    assert_fraction(gm.fraction_repeated_notes([1]), 0)
    assert_fraction(gm.fraction_repeated_notes([1, 2, 3, 4]), 0)
    assert_fraction(gm.fraction_repeated_notes([1, 2, -1, -1]), 0)
    assert_fraction(gm.fraction_repeated_notes([1, 2, 3, 1]), 1./4)
    assert_fraction(gm.fraction_repeated_notes([1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]), 9./12)
    assert_fraction(gm.fraction_repeated_notes([1, 2, -1, -1, 3, 2, 1]), 2./5)
    assert_fraction(gm.fraction_repeated_notes([1, 2, -2, -2, 3, 2, 1]), 2./5)

def test_fraction_repeated_precisely():
    assert_fraction(gm.fraction_repeated_precisely([1]), 0)
    assert_fraction(gm.fraction_repeated_precisely([1, 2, 3, 4]), 0)
    assert_fraction(gm.fraction_repeated_precisely([1, 2, 1, 2]), 0)
    assert_fraction(gm.fraction_repeated_precisely([1, 2, 1, 2], 2), 1)
    assert_fraction(gm.fraction_repeated_precisely([1, 2, 3, 2], 2), 0.5)
    assert_fraction(gm.fraction_repeated_precisely([1, 2, -2, 2], 2), 0.5)
    assert_fraction(gm.fraction_repeated_precisely([1, -1, -2, 2], 2), 0)

def test_note_mean():
    assert_fraction(gm.note_mean([-1]), 0)
    assert_fraction(gm.note_mean([-1, -2, -2, -2]), 0)
    assert_fraction(gm.note_mean([1, 2, 3]), 2)
    assert_fraction(gm.note_mean([1, 2, -2, -2, -1, 1]), 4./3)

def test_note_variance():
    assert_fraction(gm.note_variance([-1]), 0)
    assert_fraction(gm.note_variance([1]), 0)
    assert_fraction(gm.note_variance([1, 1, 1, 1]), 0)
    assert_fraction(gm.note_variance([0, 4, 0, 4]), 4)

def test_consecutive_intervals():
    assert_fraction(gm.consecutive_intervals([]), 0)
    assert_fraction(gm.consecutive_intervals([-1, -2, -1, -2]), 0)
    assert_fraction(gm.consecutive_intervals([0, 2, 4, 5]), .4/3)
    assert_fraction(gm.consecutive_intervals([0, -2, -2, 2, 4, 5]), .4/3)
    assert_fraction(gm.consecutive_intervals([0, -2, -2, 2, -1, 4, 5]), .2/2)
    assert_fraction(gm.consecutive_intervals([12, 11, 9, 7]), .4/3)


def test_syncopation():
    assert_fraction(gm.syncopation([]), 0)
    assert_fraction(gm.syncopation([1, 2, 3, 4]), 1)
    assert_fraction(gm.syncopation([1, -1, -1, -1]), 0)
    assert_fraction(gm.syncopation([1, -1, 1, -1]), 1./5)
    assert_fraction(gm.syncopation([-1, 1, -1, 1]), 4./5)
    assert_fraction(gm.syncopation([-1, -2, -2, 1]), 2./5)
    assert_fraction(gm.syncopation([1, -2, -2, -2]), 0)
    assert_fraction(gm.syncopation([-1, 1, -2, -2]), 2./5)
    assert_fraction(gm.syncopation([1, 1, 1]), 1)
    assert_fraction(gm.syncopation([-1, 1, -2]), 2./3)

def test_fraction_in_scale():
    # Major scale
    scale = {0, 2, 4, 5, 7, 9, 11}
    assert_fraction(gm.fraction_in_scale([], scale), 0)
    assert_fraction(gm.fraction_in_scale([0, 2, 4, 2], scale), 1)
    assert_fraction(gm.fraction_in_scale([0, 2, -1, 2], scale), 1)
    assert_fraction(gm.fraction_in_scale([0, 2, -2, -1], scale), 1)
    assert_fraction(gm.fraction_in_scale([0, 2, 3, 6], scale), 1./2)
    assert_fraction(gm.fraction_in_scale([0, 2, 3, -2], scale), 1./2)
    assert_fraction(gm.fraction_in_scale([12, 26, 5, 25, 37], scale), 3./5)

def test_length_mean():
    assert_fraction(gm.length_mean([]), 0)
    assert_fraction(gm.length_mean([1, 2, 3, 4]), 1)
    assert_fraction(gm.length_mean([1, -1, 3, -1]), 1)
    assert_fraction(gm.length_mean([1, -1, -2, -2]), 1)
    assert_fraction(gm.length_mean([1, -2, -2, -2]), 4)
    assert_fraction(gm.length_mean([1, -2, -1, -2]), 2)
    assert_fraction(gm.length_mean([1, 2, -2, 3, -2, -2]), 2)

def test_length_variance():
    assert_fraction(gm.length_variance([]), 0)
    assert_fraction(gm.length_variance([1, 2, 1, 0]), 0)
    assert_fraction(gm.length_variance([1, -2, -2, -2]), 0)
    assert_fraction(gm.length_variance([1, -1, -1, -1]), 0)
    assert_fraction(gm.length_variance([1, -2, 1, -2]), 0)
    assert_fraction(gm.length_variance([1, -1, -1, 1]), 0)
    assert_fraction(gm.length_variance([1, -2, -2, 2]), 1)
    assert_fraction(gm.length_variance([1, 1, -2, -2, -2, -2, 1, -2, -2, -2, -2, 1]), 4)

def main():
    test_fraction_silent()
    test_fraction_new_notes()
    test_fraction_repeated_notes()
    test_fraction_repeated_precisely()
    test_note_mean()
    test_note_variance()
    test_consecutive_intervals()
    test_syncopation()
    test_fraction_in_scale()
    test_length_mean()
    test_length_variance()

if __name__ == '__main__':
    main()
