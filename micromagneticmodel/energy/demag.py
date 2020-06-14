import ubermagutil as uu
from .energyterm import EnergyTerm


@uu.inherit_docs
class Demag(EnergyTerm):
    """Demagnetisation energy term.

    .. math::

        w_\\text{d} = -\\frac{1}{2}\\mu_{0}M_\\text{s} \\mathbf{m} \\cdot
        \\mathbf{H}_\\text{d}

    Parameters
    ----------
    asymptotic_radius : numbers.Real, optional

        Optional asymptotic radius parameter.

    Examples
    --------
    1. Defining the demagnetisation energy term.

    >>> import micromagneticmodel as mm
    ...
    >>> demag = mm.Demag()

    """
    _allowed_attributes = ['asymptotic_radius']
    _reprlatex = (r'-\frac{1}{2}\mu_{0}M_\text{s}'
                  r'\mathbf{m} \cdot \mathbf{H}_\text{d}')

    def effective_field(self, m):
        raise NotImplementedError