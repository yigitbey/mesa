'''
Mesa Space Module
=================================

Objects used to add a spatial component to a model.

Grid: base grid, a simple list-of-lists.
SingleGrid: grid which strictly enforces one object per cell.
MultiGrid: extension to Grid where each cell is a set of objects.

'''
# Instruction for PyLint to suppress variable name errors, since we have a
# good reason to use one-character variable names for x and y.
# pylint: disable=invalid-name

import itertools
import random
import math


RANDOM = -1

X = 0
Y = 1


class Grid(object):
    '''
    Base class for a grid space, composed of cells.

    Grid cells are indexed by [y][x], where [0][0] is assumed to be -- top-left
    and [height-1][width-1] is the bottom-right. If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other

    Attributes
    ----------
    width, height :  integers
        The grid's width and height.
    torus : Boolean
        Whether the edges wrap around to make the grid toroidal.
    grid : list of lists 
        Internal list-of-lists which holds the grid cells themselves.

    Methods
    -------
    get_neighbors
        Returns the objects surrounding a given cell.
    get_neighborhood
        Returns the cells surrounding a given cell.
    get_cell_list_contents 
        Returns the contents of a list of cells.
    '''
    def __init__(self, height, width, torus):
        '''Create a new grid.

        Parameters
        ----------
        height, width : int
            The height and width of the grid
        torus : Boolean
            Whether the edges wrap around to make the grid toroidal.

        '''
        self.height = height
        self.width = width
        self.torus = torus

        self.grid = []

        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.default_val())
            self.grid.append(row)

    @staticmethod
    def default_val():
        """
        Default value for new cell elements.
        """
        return None

    def __getitem__(self, index):
        return self.grid[index]

    def __iter__(self):
        # create an iterator that chains the
        #  rows of grid together as if one list:
        return itertools.chain(*self.grid)

    def coord_iter(self):
        """
        An iterator that returns coordinates as well as cell contents.
        """
        for row in range(self.height):
            for col in range(self.width):
                yield self.grid[row][col], col, row  # agent, x, y

    def neighbor_iter(self, pos, moore=True):
        """Iterate over position neighbors.

        Parameters
        ----------
        pos : (x,y) tuple 
            The position to get the neighbors of.
        moore : Boolean (default=True) 
            Whether to use Moore neighborhood (including diagonals) or 
            Von Neumann (only up/down/left/right).

        Returns
        -------
        iterator
            An iterator over the contents of the neighboring cells, not
            including the center.

        """
        neighborhood = self.iter_neighborhood(pos, moore=moore)
        return self.iter_cell_list_contents(neighborhood)

    def iter_neighborhood(self, pos, moore,
                          include_center=False, radius=1):
        """
        Return an iterator over cell coordinates that are in the
        neighborhood of a certain point.

        Parameters
        ----------
        pos : (x, y) tuple 
            Center of the neighborhood to get.
        moore :  Boolean
            Determines whether to return Moore neighborhood (including
            diagonals) if true; if False, return Von Neumann neighborhood 
            (excluding diagonals)
        include_center : Boolean (default=False)
            If True, return the center cell as well. Otherwise, return
            neighboring cells only.
        radius : int (default=1)
            Radius of cells around the center to get.

        Returns
        -------
        coord_list : list
            A list of coordinate tuples representing the neighborhood.
            With radius 1, at most 9 if Moore, 5 if Von Neumann (8 and 4 if not
            including the center).
        """
        x, y = pos
        coordinates = set()
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0 and not include_center:
                    continue
                # Skip diagonals in Von Neumann neighborhood.
                if not moore and dy != 0 and dx != 0:
                    continue
                # Skip diagonals in Moore neighborhood when distance > radius
                if moore and radius > 1 and (dy ** 2 + dx ** 2) ** .5 > radius:
                    continue
                # Skip if not a torus and new coords out of bounds.
                if not self.torus and (not (0 <= dx + x < self.width) or
                        not (0 <= dy + y < self.height)):
                    continue

                px = self.torus_adj(x + dx, self.width)
                py = self.torus_adj(y + dy, self.height)

                # Skip if new coords out of bounds.
                if(self.out_of_bounds((px, py))):
                    continue

                coords = (px, py)
                if coords not in coordinates:
                    coordinates.add(coords)
                    yield coords

    def get_neighborhood(self, pos, moore,
                         include_center=False, radius=1):
        """
        Return a list of cells that are in the
        neighborhood of a certain point.

        Parameters
        ----------
        pos : tuple
            Coordinates for the neighborhood to get.
        moore : Boolean
            If True, return Moore neighborhood (including diagonals). If False, 
            return Von Neumann neighborhood (exclude diagonals).
        include_center : Boolean (default=False)
            If True, return the (x, y) cell as well. Otherwise, return
            surrounding cells only.
        radius : int (default=1) 
            Radius, in cells, of neighborhood to get.

        Returns
        -------
        list
            A list of coordinate tuples representing the neighborhood;
            With radius 1, at most 9 if
            Moore, 5 if Von Neumann
            (8 and 4 if not including the center).
        """
        return list(self.iter_neighborhood(pos, moore, include_center, radius))

    def iter_neighbors(self, pos, moore,
                       include_center=False, radius=1):
        """
        Iterate over neighbors to a certain point.

        Parameters
        ----------
        pos : tuple
            Coordinates for the neighborhood to get.
        moore : Boolean
            If True, return Moore neighborhood (including diagonals). If False, 
            return Von Neumann neighborhood (exclude diagonals).
        include_center : Boolean (default=False)
            If True, return the (x, y) cell as well. Otherwise, return
            surrounding cells only.
        radius : int (default=1) 
            Radius, in cells, of neighborhood to get.

        Returns
        -------
        iterator
            An iterator of non-None objects in the given neighborhood; at most 
            9 if Moore, 5 if Von-Neumann (8 and 4 if not including the center).
        """
        neighborhood = self.iter_neighborhood(
            pos, moore, include_center, radius)
        return self.iter_cell_list_contents(neighborhood)

    def get_neighbors(self, pos, moore,
                      include_center=False, radius=1):
        """
        Get a list of neighbors to a certain point.

        Parameters
        ----------
        pos : tuple
            Coordinates for the neighborhood to get.
        moore : Boolean
            If True, return Moore neighborhood (including diagonals). If False, 
            return Von Neumann neighborhood (exclude diagonals).
        include_center : Boolean (default=False)
            If True, return the (x, y) cell as well. Otherwise, return
            surrounding cells only.
        radius : int (default=1) 
            Radius, in cells, of neighborhood to get.

        Returns
        -------
        list
            A list of non-None objects in the given neighborhood; at most 9 if 
            Moore, 5 if Von-Neumann (8 and 4 if not including the center).
        """
        return list(self.iter_neighbors(
            pos, moore, include_center, radius))

    def torus_adj(self, coord, dim_len):
        """
        Convert a single coordinate, handling torus looping.

        Parameters
        ----------
        coord : int
            Coordinate along an axis
        dim_len : int
            Length of the relevant axis
        """
        if self.torus:
            coord %= dim_len
        return coord

    def out_of_bounds(self, pos):
        """
        Is a position off the grid?

        Parameters
        ----------
        pos : tuple
            (x, y) tuple to check

        Returns
        -------
        Boolean
            True if the given coordinate is not on the grid; otherwise False.
        """
        x, y = pos
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def iter_cell_list_contents(self, cell_list):
        '''
        Iterate over the contents of a list of cells.

        Parameters
        ----------
        cell_list : list 
            List of (x, y) tuples

        Returns
        -------
        iterator
            A iterator of the contents of the cells identified in cell_list
        '''
        return (
            self[y][x] for x, y in cell_list if not self.is_cell_empty((x, y)))

    def get_cell_list_contents(self, cell_list):
        '''
        Get all the contents in a list of cells.

        Parameters
        ----------
        cell_list : list 
            (x, y) tuples of cells.

        Returns
        -------
        list
            All the contents of the cells identified in cell_list.
        '''
        return list(self.iter_cell_list_contents(cell_list))

    def move_agent(self, agent, pos):
        '''
        Move an agent from its current position to a new position.

        Parameters
        ----------
        agent : Agent 
            Agent to move. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        pos : tuple 
            New position to move the agent to.
        '''
        self._remove_agent(agent.pos, agent)
        self._place_agent(pos, agent)
        agent.pos = pos

    def place_agent(self, agent, pos):
        '''
        Position an agent on the grid, and set its pos variable.

        Parameters
        ----------
        agent : Agent 
            Agent to move. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        pos : Tuple 
            New position to move the agent to.
        '''
        self._place_agent(pos, agent)
        agent.pos = pos

    def _place_agent(self, pos, agent):
        '''
        Place the agent at the given location.

        Parameters
        ----------
        pos : tuple 
            New position to place the agent at.
        agent : Agent 
            Agent to place. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        '''
        x, y = pos
        self.grid[y][x] = agent

    def _remove_agent(self, pos, agent):
        '''
        Remove the agent from the given location.

        Parameters
        ----------
        pos : tuple 
            Position to remove the agent from.
        agent : Agent 
            Agent to remove from grid.
        '''
        x, y = pos
        self.grid[y][x] = None

    def is_cell_empty(self, pos):
        '''
        Check whether a given cell is empty.

        Parameters
        ----------
        pos : tuple
            Coordinates of cell to check.
        '''
        x, y = pos
        return True if self.grid[y][x] == self.default_val() else False


class SingleGrid(Grid):
    '''
    Grid where each cell contains exactly at most one object.
    '''
    empties = []

    def __init__(self, height, width, torus):
        '''
        Create a new single-item grid.

        Parameters
        ----------
        height, width : int 
            The height and width of the grid
        torus : Boolean 
            Whether the grid wraps or not.
        '''
        super().__init__(height, width, torus)
        # Add all cells to the empties list.
        self.empties = list(itertools.product(
                            *(range(self.width), range(self.height))))

    def move_to_empty(self, agent):
        """
        Moves agent to a random empty cell, vacating agent's old cell.

        Parameters
        ----------
        agent : Agent
            Agent to move
        """
        pos = agent.pos
        new_pos = self.find_empty()
        if new_pos is None:
            raise Exception("ERROR: No empty cells")
        else:
            self._place_agent(new_pos, agent)
            agent.pos = new_pos
            self._remove_agent(pos, agent)

    def find_empty(self):
        '''
        Pick a random empty cell.

        Returns
        -------
        tuple
            An (x, y) tuple of a randomly-selected empty cell.
        '''
        if self.exists_empty_cells():
            pos = random.choice(self.empties)
            return pos
        else:
            return None

    def exists_empty_cells(self):
        """
        Returns
        -------
        Boolean
            True if any empty cell exists.
        """
        return len(self.empties) > 0

    def position_agent(self, agent, pos=None):
        """
        Place a new agent on the grid.

        Parameters
        ----------
        agent : Agent
            The agent to place.
        pos : tuple (default=None)
            Coordinate to place the agent. If None, the agent will be placed on
            a random empty cell.
        """
        if pos is None:
            coords = self.find_empty()
            if coords is None:
                raise Exception("ERROR: Grid full")
        agent.pos = pos
        self._place_agent(pos, agent)

    def _place_agent(self, pos, agent):
        '''
        Place the agent at the given location, making sure it's empty.

        Parameters
        ----------
        pos : Tuple 
            New position to place the agent at.
        agent : Agent 
            Agent to move. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        '''
        if self.is_cell_empty(pos):
            super()._place_agent(pos, agent)
            self.empties.remove(pos)
        else:
            raise Exception("Cell not empty")

    def _remove_agent(self, pos, agent):
        '''
        Remove the agent from the given location.

        Parameters
        ----------
        pos : Tuple 
            Position to remove the agent from.
        agent : Agent 
            Agent to remove from grid.
        '''
        super()._remove_agent(pos, agent)
        self.empties.append(pos)


class MultiGrid(Grid):
    '''
    Grid where each cell can contain more than one object.

    Grid cells are indexed by [y][x], where [0][0] is assumed to be -- top-left
    and [height-1][width-1] is the bottom-right. If a grid is toroidal, the top
    and bottom, and left and right, edges wrap to each other.

    Each grid cell holds a set object.

    Attributes
    ----------
    width, height :  integers
        The grid's width and height.
    torus : Boolean
        Whether the edges wrap around to make the grid toroidal.
    grid : list of lists 
        Internal list-of-lists which holds the grid cells themselves.

    Methods
    -------
    get_neighbors
        Returns the objects surrounding a given cell.
    get_neighborhood
        Returns the cells surrounding a given cell.
    get_cell_list_contents 
        Returns the contents of a list of cells.
    '''

    @staticmethod
    def default_val():
        """
        Default value for new cell elements.
        """
        return set()

    def _place_agent(self, pos, agent):
        '''
        Add the agent to the given location.

        Parameters
        ----------
        pos : Tuple 
            New position to place the agent at.
        agent : Agent 
            Agent to move. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        '''
        x, y = pos
        self.grid[y][x].add(agent)

    def _remove_agent(self, pos, agent):
        '''
        Remove the agent from the given location.

        Parameters
        ----------
        pos : Tuple 
            Position to remove the agent from.
        agent : Agent 
            Agent to remove from grid.
        '''
        x, y = pos
        self.grid[y][x].remove(agent)

    def iter_cell_list_contents(self, cell_list):
        '''
        Iterate over the contents of a list of cells.

        Parameters
        ----------
        cell_list : list 
            List of (x, y) tuples

        Returns
        -------
        iterator
            A iterator of the contents of the cells identified in cell_list
        '''
        return itertools.chain.from_iterable(
            self[y][x] for x, y in cell_list if not self.is_cell_empty((x, y)))


class ContinuousSpace(object):
    '''
    Continuous space where each agent can have an arbitrary position.

    Assumes that all agents are point objects, and have a pos property storing
    their position as an (x, y) tuple. This class uses a MultiGrid internally
    to store agent objects, to speed up neighborhood lookups.
    '''

    _grid = None

    def __init__(self, x_max, y_max, torus, x_min=0, y_min=0,
                 grid_width=100, grid_height=100):
        '''
        Create a new continuous space.

        Parameters
        ----------
        x_max, y_max : float
            Maximum x and y coordinates for the space.
        torus : Boolean 
            Whether the edges loop around.
        x_min, y_min : float (default=0) 
            If provided, set the minimum x and y coordinates for the space.
            Below them, values loop to the other edge (if torus=True) or raise 
            an exception.
        grid_width, grid_height : int (default=100) 
            Determine the size of the internal storage grid. More cells will
            slow down movement, but speed up neighbor lookup. Probably only
            fiddle with this if one or the other is impacting your model's 
            performance.
        '''
        self.x_min = x_min
        self.x_max = x_max
        self.width = x_max - x_min
        self.y_min = y_min
        self.y_max = y_max
        self.height = y_max - y_min
        self.torus = torus

        self.cell_width = (self.x_max - self.x_min) / grid_width
        self.cell_height = (self.y_max - self.y_min) / grid_height

        self._grid = MultiGrid(grid_height, grid_width, torus)

    def place_agent(self, agent, pos):
        '''
        Place a new agent in a given point in the space.

        Parameters
        ----------
        agent : Agent 
            Agent to move. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        pos : Tuple 
            New position to move the agent to.
        '''
        pos = self.torus_adj(pos)
        self._place_agent(pos, agent)
        agent.pos = pos

    def move_agent(self, agent, pos):
        '''
        Move an agent from its current position to a new position.

        Parameters
        ----------
        agent : Agent 
            Agent to move. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        pos : tuple 
            New position to move the agent to.
        '''
        pos = self.torus_adj(pos)
        self._remove_agent(agent.pos, agent)
        self._place_agent(pos, agent)
        agent.pos = pos

    def _place_agent(self, pos, agent):
        '''
        Place an agent at a given point, and update the internal grid.

        Parameters
        ----------
        pos : tuple 
            New position to place the agent at.
        agent : Agent 
            Agent to place. Assumed to have its current location stored as a
            tuple in a 'pos' property.
        '''
        cell = self._point_to_cell(pos)
        self._grid._place_agent(cell, agent)

    def _remove_agent(self, pos, agent):
        '''
        Remove an agent at a given point, and update the internal grid.

        Parameters
        ----------
        pos : tuple 
            Position to remove the agent from.
        agent : Agent 
            Agent to remove from grid.
        '''
        cell = self._point_to_cell(pos)
        self._grid._remove_agent(cell, agent)

    def get_neighbors(self, pos, radius, include_center=True):
        '''
        Get all objects within a certain radius.

        Parameters
        ----------
        pos : tuple 
            (x,y) coordinate tuple to center the search at.
        radius : float 
            Get all the objects within this distance of the center.
        include_center : Boolean (default=True) 
            If True, include an object at the *exact* provided coordinates. 
            i.e. if you are searching for the neighbors of a given agent, True
            will include that agent in the results.

        Returns
        -------
        list
            A list of objects in the space within the radius from the center.
        '''
        # Get candidate objects
        scale = max(self.cell_width, self.cell_height)
        cell_radius = math.ceil(radius / scale)
        cell_pos = self._point_to_cell(pos)
        possible_objs = self._grid.get_neighbors(cell_pos,
                                              True, True, cell_radius)
        neighbors = []
        # Iterate over candidates and check actual distance.
        for obj in possible_objs:
            dist = self.get_distance(pos, obj.pos)
            if dist <= radius and (include_center or dist > 0):
                neighbors.append(obj)
        return neighbors

    def get_distance(self, pos_1, pos_2):
        '''
        Get the distance between two point, accounting for toroidal space.

        Parameters
        ----------
        pos_1, pos_2 : tuples 
            Coordinate tuples for both points.

        Returns
        -------
            Euclidean distance between the two points.
        '''
        x1, y1 = pos_1
        x2, y2 = pos_2
        if not self.torus:
            dx = x1 - x2
            dy = y1 - y2
        else:
            d_x = abs(x1 - x2)
            d_y = abs(y1 - y2)
            dx = min(d_x, self.width - d_x)
            dy = min(d_y, self.height - d_y)
        return math.sqrt(dx ** 2 + dy ** 2)

    def torus_adj(self, pos):
        '''
        Adjust coordinates to handle torus looping.

        Parameters
        ----------
        pos : tuple
            Coordinate tuple to convert

        Returns
        -------
        tuple
            If the coordinate is out-of-bounds and the space is toroidal,
            return the corresponding point within the space. If the space is
            not toroidal, raise an exception.
        '''
        if not self.out_of_bounds(pos):
            return pos
        elif not self.torus:
            raise Exception("Point out of bounds, and space non-toroidal.")
        else:
            x = self.x_min + ((pos[0] - self.x_min) % self.width)
            y = self.y_min + ((pos[1] - self.y_min) % self.height)
            return (x, y)

    def _point_to_cell(self, pos):
        '''
        Get the coordinates of the internal grid cell that a point falls into.

        Parameters
        ----------
        pos : tuple
            Spatial (x, y) coordinates.

        Returns
        -------
        tuple
            A tuple of the grid coordinates the point corresponds with.
        '''
        if self.out_of_bounds(pos):
            raise Exception("Point out of bounds.")

        x, y = pos
        cell_x = math.floor((x - self.x_min) / self.cell_width)
        cell_y = math.floor((y - self.y_min) / self.cell_height)
        return (cell_x, cell_y)

    def out_of_bounds(self, pos):
        '''
        Check if a point is out of bounds.

        Parameters
        ----------
        pos : tuple
            (x, y) tuple to check

        Returns
        -------
        Boolean
            True if the given coordinate is not on the grid; otherwise False.

        '''
        x, y = pos
        return (x < self.x_min or x > self.x_max or
                y < self.y_min or y > self.y_max)
