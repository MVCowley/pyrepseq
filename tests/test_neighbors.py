from pyrepseq.neighbors import *

def test_levenshtein():
    neighbors = list(levenshtein_neighbors('A'))
    # deletion
    assert '' in neighbors
    # replacement
    assert 'C' in neighbors
    # insertions
    assert 'CA' in neighbors
    assert 'AC' in neighbors
    # uniqueness
    assert len(neighbors) == len(set(neighbors))

def test_hamming():
    neighbors = list(hamming_neighbors('A'))
    # replacement
    assert 'C' in neighbors
    # correct length
    assert len(neighbors) == (len(aminoacids)-1)