import importlib
import discretisedfield as df
import micromagneticmodel as mm
import joommfutil.typesystem as ts


@ts.typesystem(name=ts.ObjectName)
class System:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ["hamiltonian", "dynamics", "m", "name"]:
                setattr(self, key, value)
            else:
                raise AttributeError("Unexpected kwarg {}.".format(key))

        self.selfmodule = importlib.__import__(self.__class__.__module__)
        if "hamiltonian" not in self.__dict__:
            self.hamiltonian = 0
        if "dynamics" not in self.__dict__:
            self.dynamics = 0

    @property
    def mesh(self):
        raise ValueError("Mesh is not a part of system any more.")

    @mesh.setter
    def mesh(self, value):
        raise ValueError("Mesh must not be a part of system any more.")

    @property
    def hamiltonian(self):
        return self._hamiltonian

    @hamiltonian.setter
    def hamiltonian(self, value):
        if value == 0:
            self._hamiltonian = self.selfmodule.Hamiltonian()
        elif isinstance(value, mm.Hamiltonian):
            self._hamiltonian = value
        elif isinstance(value, mm.EnergyTerm):
            hamiltonian = self.selfmodule.Hamiltonian()
            hamiltonian += value
            self._hamiltonian = hamiltonian
        else:
            raise TypeError("Expected EnergyTerm or Hamiltonian.")

    @property
    def dynamics(self):
        return self._dynamics

    @dynamics.setter
    def dynamics(self, value):
        if value == 0:
            self._dynamics = self.selfmodule.Dynamics()
        elif isinstance(value, mm.Dynamics):
            self._dynamics = value
        elif isinstance(value, mm.DynamicsTerm):
            dynamics = self.selfmodule.Dynamics()
            dynamics += value
            self._dynamics = dynamics
        else:
            raise TypeError("Expected DynamicsTerm or Dynamics.")

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        if isinstance(value, df.Field):
            self._m = value
        else:
            raise TypeError("Unsupported type(m)={}".format(type(value)))

    def script(self):
        raise NotImplementedError
