"""veritas-holo: a falsifiable geometric reasoning substrate. v0.1 is a mathematical reference
implementation only; see README.md for what it does and does not claim."""
from .algebra import (commutator, det_error, expi, group_commutator, holonomy_loop, random_diagonal_hermitian,
                      random_hermitian, unitarity_error)
from .states import InvariantReport, Trajectory, check_norm_preserved, distance, random_state, run_trajectory

__version__ = "0.1.0"
__all__ = ["commutator", "det_error", "expi", "group_commutator", "holonomy_loop", "random_diagonal_hermitian",
           "random_hermitian", "unitarity_error", "InvariantReport", "Trajectory", "check_norm_preserved",
           "distance", "random_state", "run_trajectory"]
