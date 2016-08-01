from micromagneticmodel.dynamics import DynamicsTerm
from micromagneticmodel.util.typesystem import UnsignedReal, String, typesystem


@typesystem(alpha=UnsignedReal,
            name=String)
class Damping(DynamicsTerm):
    def __init__(self, alpha, name='damping'):
        """A damping dynamics term class.

        Args:
            alpha (Real): Gilbert damping

        """
        self.alpha = alpha
        self.name = name
        self.latex_str = ('$\\alpha \mathbf{m} \\times'
                          '\\frac{\partial \mathbf{m}}{\partial t}$')

    @property
    def _repr_str(self):
        """A representation string property.

        Returns:
           A representation string.

        """
        return 'Damping(alpha={})'.format(self.alpha)
