"""An abstraction of canvas, on which the bodies interact with eachother."""

import pygame

from threeBodyProblem.objects.body import Body
from threeBodyProblem.constants import COLORS, PYGAME_CONSTANTS


class Canvas:
    """
    Abstraction representing the sky, on which the bodies interact.
    Responsible for updating the bodies' positions and displaying other
    features.
    """

    def __init__(self, win: pygame.Surface):
        self._win = win
        self._bodies = []
        self._show_vectors = False
        self._show_trails = True
        self._show_graph = True

    # ============= PRIVATE METHODS ============= #

    def _plot_graph(self) -> None:
        """
        Plot the graph of the bodies' positions.
        """
        # Draw the axes
        graph_center = (
            PYGAME_CONSTANTS.GRAPH_PADDING,
            PYGAME_CONSTANTS.HEIGHT - PYGAME_CONSTANTS.GRAPH_PADDING
        )
        pygame.draw.line(
            self._win,
            COLORS.WHITE,
            graph_center,
            (
                graph_center[0] + PYGAME_CONSTANTS.GRAPH_WIDTH,
                graph_center[1]
            ),
            PYGAME_CONSTANTS.GRAPH_THICKNESS
        )
        pygame.draw.line(
            self._win,
            COLORS.WHITE,
            graph_center,
            (
                graph_center[0],
                graph_center[1] - PYGAME_CONSTANTS.GRAPH_HEIGHT
            ),
            PYGAME_CONSTANTS.GRAPH_THICKNESS
        )
        # Draw the trails
        for body in self._bodies:
            body.plot_on_graph()

    # ============= PUBLIC METHODS =============== #

    def toggle_vectors_display(self) -> None:
        """
        Switch between displaying bodies' vectors and not doing that.
        """
        self._show_vectors = not self._show_vectors

    def toggle_draw_trails(self) -> None:
        """
        Switch between drawing trails and not doing that.
        """
        self._show_trails = not self._show_trails

    def toggle_plot_graph(self) -> None:
        """
        Switch between plotting the graph and not doing that.
        """
        self._show_graph = not self._show_graph
    
    def reset(self) -> None:
        """
        Reset the canvas.
        """
        self._bodies = []

    def draw(self) -> None:
        """
        Draw the canvas.
        """
        self._win.fill(COLORS.BLACK)

        for body in self._bodies:
            body.draw(self._show_vectors, self._show_trails)

        if self._show_graph:
            self._plot_graph()

    def add_body(
        self,
        number: int,
        mass: float,
        init_x: int,
        init_y: int,
        init_vector: list[float],
        is_stationary: bool = False,
    ) -> None:
        """
        Initialize and add a body to the canvas.

        Args:
            win(pygame.Surface): the window on which the body is drawn
            mass(float): the mass of the body
            init_x(int): the initial x coordinate of the body
            init_y(int): the initial y coordinate of the body
            init_vector(list[float]): the initial velocity vector of the body
            is_stationary(bool): whether the body is stationary or not
        """
        self._bodies.append(
            Body(
                number,
                self._win,
                mass,
                init_x,
                init_y,
                init_vector,
                is_stationary
            )
        )

    def update(self) -> None:
        """
        Update the positions of the bodies and draw them.
        """
        for body1 in self._bodies:
            for body2 in self._bodies:
                if body1 == body2:
                    continue
                body1.calculate_impact_on(body2)

            body1.update()
