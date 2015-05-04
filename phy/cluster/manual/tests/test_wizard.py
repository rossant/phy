# -*- coding: utf-8 -*-

"""Test wizard."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

from pytest import raises

from ..wizard import (_previous,
                      _next,
                      Wizard,
                      WizardPanel,
                      )


#------------------------------------------------------------------------------
# Test wizard
#------------------------------------------------------------------------------

def test_utils():
    l = [2, 3, 5, 7, 11]

    func = lambda x: x in (2, 5)

    with raises(RuntimeError):
        _previous(l, 1, func)
    with raises(RuntimeError):
        _previous(l, 15, func)

    assert _previous(l, 2, func) == 2
    assert _previous(l, 3, func) == 2
    assert _previous(l, 5, func) == 2
    assert _previous(l, 7, func) == 5
    assert _previous(l, 11, func) == 5

    with raises(RuntimeError):
        _next(l, 1, func)
    with raises(RuntimeError):
        _next(l, 15, func)

    assert _next(l, 2, func) == 5
    assert _next(l, 3, func) == 5
    assert _next(l, 5, func) == 5
    assert _next(l, 7, func) == 7
    assert _next(l, 11, func) == 11


def test_core_wizard():

    wizard = Wizard([2, 3, 5])

    @wizard.set_quality_function
    def quality(cluster):
        return {2: .9,
                3: .3,
                5: .6,
                }[cluster]

    @wizard.set_similarity_function
    def similarity(cluster, other):
        cluster, other = min((cluster, other)), max((cluster, other))
        return {(2, 3): 1,
                (2, 5): 2,
                (3, 5): 3}[cluster, other]

    assert wizard.best_clusters() == [2, 5, 3]
    assert wizard.best_clusters(n_max=0) == [2, 5, 3]
    assert wizard.best_clusters(n_max=None) == [2, 5, 3]
    assert wizard.best_clusters(n_max=2) == [2, 5]

    assert wizard.best_cluster() == 2

    assert wizard.most_similar_clusters() == [5, 3]
    assert wizard.most_similar_clusters(2) == [5, 3]

    assert wizard.most_similar_clusters(n_max=0) == [5, 3]
    assert wizard.most_similar_clusters(n_max=None) == [5, 3]
    assert wizard.most_similar_clusters(n_max=1) == [5]


def test_panel():
    panel = WizardPanel()
    assert panel.html

    panel.best = 3
    assert panel.html

    panel.match = 10
    assert panel.html
