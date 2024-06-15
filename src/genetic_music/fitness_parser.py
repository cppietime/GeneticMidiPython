from .fitness import *

names = {
    "silent": fraction_silent,
    "new_notes": fraction_new_notes,
    "repeated_notes": fraction_repeated_notes,
    "repeated_precisely": fraction_repeated_precisely,
    "note_mean": note_mean,
    "note_variance": note_variance,
    "consecutive_intervals": consecutive_intervals,
    "syncopation": syncopation,
    "in_scale": fraction_in_scale,
    "length_mean": length_mean,
    "length_variance": length_variance
}

def parse_fitness(func_list):
    funcs = []
    for segment in func_list:
        func_name = segment['function']
        func = names[func_name]
        weight = segment['weight']
        bias = segment['bias']
        args = segment.get('args', {})
        term = lambda pop, func=func, weight=weight, bias=bias, args=args:\
            -abs(func(pop, **args) - bias) * weight
        funcs.append(term)
    fitness = lambda pop:\
        sum(map(lambda x: x(pop), funcs))
    return fitness
        
