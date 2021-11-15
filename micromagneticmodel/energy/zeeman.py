import ubermagutil as uu
import discretisedfield as df
import ubermagutil.typesystem as ts
from .energyterm import EnergyTerm


@uu.inherit_docs
@ts.typesystem(H=ts.Parameter(descriptor=ts.Vector(size=3),
                              otherwise=df.Field),
               wave=ts.Subset(sample_set={'sin', 'sinc'}, unpack=False),
               f=ts.Scalar(positive=True),
               t0=ts.Scalar(),
               # time_dependence=ts.Typed(expected_type=callable),
               tstep=ts.Scalar(positive=True),
               tcl_strings=ts.Dictionary(
                   key_descriptor=ts.Subset(
                       sample_set=('script', 'energy', 'type', 'script_args',
                                   'script_name'), unpack=False),
                   value_descriptor=ts.Typed(expected_type=str))
               )
class Zeeman(EnergyTerm):
    r"""Zeeman energy term.

    .. math::

        w = -\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}

    Zeeman energy term allows defining time-dependent as well as
    time-independent external magnetic field. If only external magnetic field
    ``H`` is passed, a time-constant field is defined.

    Three different methods are available to define a time-dependent field:

    - pre-defined ``sine`` wave and ``sinc`` pulse
    - custom time-dependence via Python callable
    - custom ``tcl`` code passed directly to OOMMF

    There are two built-in functions to specify a time-dependent field. To use
    these ``wave`` must be passed as a string. ``wave`` can be either
    ``'sine'`` or ``'sinc'``. If time-dependent external magnetic field is
    defined using ``wave``, ``f`` and ``t0`` must be passed. For
    ``wave='sine'``, energy density is:

    .. math::

        w = -\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H} \sin[2\pi
        f(t-t_{0})]

    whereas for ``wave='sinc'``, the energy density is:

    .. math::

        w = -\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}
        \text{sinc}[2\pi f(t-t_{0})]

    and ``f`` is a cut-off frequency.

    Arbitrary time-dependence can be specified by passing a callable to
    ``time_dependence``. Additionally ``tstep`` in seconds must be provided.
    The function is evaluated at all time steps separated by ``tstep`` (up to
    the desired run-time). Additionally, the derivative is computed internally
    (using central differences). Therefore, the function has to be derivable.
    In order for this method to be stable a reasonable small time-step must be
    chosen. As a rough guideline start around 1e-13s. The callable passed to
    ``time_dependence`` must either return a single number that is used to
    multiply the initial field or a list of nine values that define a matrix
    ``M`` that is multiplied with the initial field vector. Ordering of the
    matrix elements is ``[M11, M12, M12, M21, M22, M23, M31, M32, M33]``. The
    matrix allows for more complicated processes, e.g. a rotating field.

    To have more control and use the full flexibility of OOMMF it is also
    possible to directly pass several tcl strings that are added to the ``mif``
    file without further modification. Please refer to the OOMMF documentation
    The dictionary must be passed to ``tcl_strings`` and must contain ``proc``,
    ``energy``, ``type``, ``script_args``, and ``script``. Please refer to the
    OOMMF documentation for detailed explanations. Generally, specifying
    ``time_dependence`` and ``tstep`` is easier for the user.

    Parameters
    ----------
    H : (3,) array_like, dict, discretisedfield.Field

        If a single length-3 array_like (tuple, list, ``numpy.ndarray``) is
        passed, which consists of ``numbers.Real``, a spatially constant
        parameter is defined. For a spatially varying parameter, either a
        dictionary, e.g. ``H={'region1': (0, 0, 3e6), 'region2': (0, 0,
        -3e6)}`` (if the parameter is defined "per region") or
        ``discretisedfield.Field`` is passed.

    wave : str, optional

        For a time dependent field, either ``'sine'`` or ``'sinc'`` is passed.

    f : numbers.Real, optional (required for ``wave``)

        (Cut-off) frequency in Hz.

    t0 : numbers.Real, optional (required for ``wave``)

        Time for adjusting the phase (time-shift) of a wave.

    time_dependence : callable, optional

        Callable to define arbitrary time-dependence. Called at times that are
        multiples of ``tstep``. Must return either a single number or a list of
        nine values.

    tstep : numbers.Real, optional (required for ``time_dependence``)

        Time steps in seconds to evaluate callable ``time_dependence`` at.

    tcl_strings : dict, optional

        Dictionary of ``tcl`` strings to be included into the ``mif`` file for
        more control over specific time-dependencies. Must contain the
        following keys: ``proc``, ``energy``, ``type``, ``script_args``, and
        ``script`` (name of the script).

    Examples
    --------
    1. Defining the Zeeman energy term using a vector.

    >>> import micromagneticmodel as mm
    ...
    >>> zeeman = mm.Zeeman(H=(0, 0, 1e6))

    2. Defining the Zeeman energy term using dictionary.

    >>> zeeman = mm.Zeeman(H={'region1': (0, 0, 1e6), 'region2': (0, 0, -1e6)})

    3. Defining the Zeeman energy term using ``discretisedfield.Field``.

    >>> import discretisedfield as df
    ...
    >>> region = df.Region(p1=(0, 0, 0), p2=(5e-9, 5e-9, 10e-9))
    >>> mesh = df.Mesh(region=region, n=(5, 5, 10))
    >>> H = df.Field(mesh, dim=3, value=(1e6, -1e6, 0))
    >>> zeeman = mm.Zeeman(H=H)

    4. Defining the Zeeman energy term using a vector which changes as a sine
    wave.

    >>> zeeman = mm.Zeeman(H=(0, 0, 1e6), wave='sin', f=1e9, t0=0)

    5. An attempt to define the Zeeman energy term using a wrong value.

    >>> zeeman = mm.Zeeman(H=(0, -1e7))  # length-2 vector
    Traceback (most recent call last):
    ...
    ValueError: ...

    """

    _allowed_attributes = ['H', 'wave', 'f', 't0', 'time_dependence', 'tstep',
                           'tcl_strings']

    @property
    def _reprlatex(self):
        if self.wave == 'sin':
            return (r'-\mu_{0}M_\text{s} \mathbf{m}'
                    r'\cdot \mathbf{H} \sin[2 \pi f (t-t_{0})]')
        elif self.wave == 'sinc':
            return (r'-\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}\, '
                    r'\text{sinc}[2 \pi f (t-t_{0})]')
        else:
            return r'-\mu_{0}M_\text{s} \mathbf{m} \cdot \mathbf{H}'

    def effective_field(self, m):
        raise NotImplementedError
