import numpy as np

from avito_dups.groups import pair_groups


def test_pair_groups_joins_pairs_through_shared_items():
    first = np.array([1000, 1000, 7000, 50000])
    second = np.array([7000, 9000, 20000, 60000])
    groups = pair_groups(first, second)
    assert len(groups) == 4
    assert groups[0] == groups[1] == groups[2]
    assert groups[3] != groups[0]


def test_pair_groups_ignores_slot_of_shared_item():
    first = np.array([1, 3])
    second = np.array([2, 1])
    groups = pair_groups(first, second)
    assert groups[0] == groups[1]
