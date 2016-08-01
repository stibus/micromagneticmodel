import pytest
from micromagneticmodel.hamiltonian import Demag


class TestDemag(object):
    def test_repr_latex_(self):
        demag = Demag()
        latex_str = demag._repr_latex_()

        # Assert some characteristics of LaTeX string.
        assert isinstance(latex_str, str)
        assert latex_str[0] == latex_str[-1] == '$'
        assert '\\mu_{0}' in latex_str
        assert '\mathbf{H}_\\text{d}' in latex_str
        assert '\mathbf{m}' in latex_str
        assert '\cdot' in latex_str
        assert 'M_\\text{s}' in latex_str
        assert '\\frac{1}{2}' in latex_str

    def test_abstract_script_method(self):
        with pytest.raises(NotImplementedError):
            demag = Demag()
            demag.script()

    def test_name(self):
        demag = Demag()

        assert demag.name == 'demag'

    def test_repr(self):
        demag = Demag()

        assert repr(demag) == 'Demag()'

    def test_script(self):
        demag = Demag()
        with pytest.raises(NotImplementedError):
            demag.script()
