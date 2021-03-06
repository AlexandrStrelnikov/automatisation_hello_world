
from lib2.IQPulseSequence import *
from lib2.VNATimeResolvedDispersiveMeasurement1D import *
from lib2.DispersiveRamsey import *

class DispersiveHahnEcho(VNATimeResolvedDispersiveMeasurement1D):

    def __init__(self, name, sample_name, **devs_aliases_map):
        super().__init__(name, sample_name, devs_aliases_map)

        self._measurement_result = DispersiveHahnEchoResult(name, sample_name)
        self._sequence_generator = IQPulseBuilder.build_dispersive_hahn_echo_sequences
        self._swept_parameter_name = "echo_delay"

    def set_swept_parameters(self, echo_delays):
        super().set_swept_parameters(self._swept_parameter_name, echo_delays)

class DispersiveHahnEchoResult(VNATimeResolvedDispersiveMeasurement1DResult):

    def _model(self, t, A_r, A_i, T_2_ast, offset_r, offset_i):
        return (A_r+1j*A_i)*exp(-1/T_2_ast*t)+(offset_r+1j*offset_i)

    def _generate_fit_arguments(self, x, data):
        p0=[-ptp(real(data)), -ptp(imag(data)), 1, max(real(data)), max(imag(data))]
        bounds =([-5, -5, 0.1, -5, -5], [5, 5, 20, 5, 5])
        return p0, bounds

    def _generate_annotation_string(self, opt_params, err):
        return "$T_{2E}=%.2f \pm %.2f \mu$s"%(opt_params[2], err[2])
