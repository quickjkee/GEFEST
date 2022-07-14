import numpy as np

from gefest.core.structure.structure import Structure
from gefest.tools.estimators.DL.bw_surrogate.bw_cnn import CNN
from gefest.tools.estimators.simulators.swan.swan_interface import Swan
from gefest.tools.estimators.estimator import Estimator
import cases.breakwaters.configuration_de.bw_domain as area


def configurate_estimator(domain):
    # ------------
    # User-defined estimator
    # it should be created as object with .estimate() method
    # ------------
    path = '../../gefest/tools/estimators/simulators/swan/swan_model/'
    swan = Swan(path=path,
                targets=area.targets,
                grid=area.grid,
                domain=domain)
    cnn = CNN(domain=domain,
              main_model=swan)

    # Multi-criteria loss function, in our case - HW and cost of structure
    def loss(struct: Structure, estimator):
        max_length = np.linalg.norm(
            np.array([max(area.coord_X) - min(area.coord_X), max(area.coord_Y) - min(area.coord_Y)]))
        lengths = 0
        for poly in struct.polygons:
            if poly.id != 'fixed':
                length = domain.geometry.get_length(poly)
                lengths += length

        hs = estimator.estimate(struct)
        l_f = [hs, 2 * lengths / max_length]

        return l_f

    # ------------
    # GEFEST estimator
    # ------------

    # Here loss is an optional argument, otherwise estimator will be considered as loss for minimizing
    estimator = Estimator(estimator=cnn,
                          loss=loss)

    return estimator
