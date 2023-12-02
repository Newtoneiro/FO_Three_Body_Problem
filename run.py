"""Main file presenting the whole program in action."""

import pygame

from threeBodyProblem.simulation import Simulation
from threeBodyProblem.simulation_params import SimulationParams
from threeBodyProblem.constants import PYGAME_CONSTANTS, COLORS


class SimulationManager:
    """
    Class managing the simulations.
    """

    # ============== INITIALIZATION =============== #

    def __init__(
            self,
            ) -> None:
        self._init_pygame()
        self._init_enviroment()
        self._init_simulations()

    def _init_pygame(self) -> None:
        """
        Initializes pygame.
        """
        pygame.init()
        pygame.display.set_caption(PYGAME_CONSTANTS.WINDOW_TITLE)
        self._win = pygame.display.set_mode(
            (PYGAME_CONSTANTS.WIDTH, PYGAME_CONSTANTS.HEIGHT)
        )
        self._clock = pygame.time.Clock()

    def _init_enviroment(self) -> None:
        """
        Initializes the enviroment.
        """
        self._last_pos_clicked = [0, 0]
        self._run = True

    def _init_simulations(self) -> None:
        """
        Initializes the simulations.
        """
        self._simulations = [
            Simulation(
                self._win,
                self._clock,
                SimulationParams(255, 400, 1000, 0.40)
            ),
            Simulation(
                self._win,
                self._clock,
                SimulationParams(50, 400, 1000, 0.400001)
            ),
        ]

    def _handle_events(self) -> None:
        """
        Handles all events.
        """
        for event in pygame.event.get():
            self._event_callbacks.get(event.type, lambda _: None)(event)

    def _init_event_callbacks(self) -> None:
        """
        Initializes pygame callbacks.
        """
        self._event_callbacks = {
            pygame.QUIT: lambda event: self._handle_stop(event),
            pygame.KEYDOWN: lambda event: self._handle_key_down(event),
        }

        self._key_callbacks = {
            pygame.K_v: self._handle_show_vectors,
            pygame.K_t: self._handle_switch_draw_trails,
            pygame.K_g: self._handle_switch_plot_graph,
            pygame.K_r: self._handle_reset,
        }

    # ================== EVENT HANDLERS ================== #

    def _handle_stop(self, event: pygame.event.Event) -> None:
        """
        Stops the simulation.
        """
        self._run = False

    def _handle_key_down(self, event: pygame.event.Event) -> None:
        """
        Handles key down event.
        """
        self._key_callbacks.get(event.key, lambda: None)()

    # ================== KEY CALLBACKS ================== #

    def _handle_show_vectors(self) -> None:
        """
        Handles show vectors event.
        """
        for simulation in self._simulations:
            simulation.toggle_show_vectors()

    def _handle_switch_draw_trails(self) -> None:
        """
        Handles switch draw trails event.
        """
        for simulation in self._simulations:
            simulation.toggle_draw_trails()

    def _handle_switch_plot_graph(self) -> None:
        """
        Handles switch plot graph event.
        """
        for simulation in self._simulations:
            simulation.toggle_show_graph()

    def _handle_reset(self) -> None:
        """
        Handles reset event.
        """
        for simulation in self._simulations:
            simulation.reset()

    # ================== PUBLIC METHODS ================== #

    def run(self) -> None:
        """
        Runs the simulations.
        """
        self._init_event_callbacks()
        while self._run:
            self._clock.tick(PYGAME_CONSTANTS.FPS)
            self._win.fill(COLORS.BACKGROUND_COLOR)
            for simulation in self._simulations:
                simulation.run()
            self._handle_events()
            pygame.display.flip()


if __name__ == "__main__":
    sm = SimulationManager()
    sm.run()
