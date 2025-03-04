from collections import defaultdict  # Import defaultdict to manage the adjacency list of the constraint graph.

class CSP:
    """
    The CSP (Constraint Satisfaction Problem) class encapsulates the functionality of a generic CSP solver.
    - Variables represent the nodes of the graph.
    - Constraints are rules that define valid relationships between variables.
    - The constraint graph represents the connections between variables based on constraints.
    """

    def __init__(self):
        """
        Initializes the CSP instance with:
        - variables: Dictionary mapping variables to their domains. Each variable is associated with a list of possible values.
        - constraints: List of constraints as tuples (variables, constraint function).
        - constraint_graph: Adjacency list representing connections between variables based on constraints.
        """
        self.variables = {}  # Holds variables as keys and their domains as values.
        self.constraints = []  # Stores constraints as a list of (variables, constraint function) tuples.
        self.constraint_graph = defaultdict(set)  # Represents the graph where variables are nodes and edges are constraints.

    def add_variable(self, var, domain):
        """
        Adds a variable to the CSP with a specified domain.
        - var: The variable to add (e.g., (row, col) for a cell).
        - domain: The list of possible values for this variable.
        """
        self.variables[var] = domain  # Add the variable and its domain to the variables dictionary.

    def add_constraint(self, variables, constraint_fn):
        """
        Adds a constraint to the CSP.
        - variables: List of variables that the constraint applies to.
        - constraint_fn: A function defining the constraint logic.
        """
        self.constraints.append((variables, constraint_fn))  # Add the constraint to the list.
        for var1 in variables:  # For each pair of variables in the constraint,
            for var2 in variables:
                if var1 != var2:  # If they are distinct,
                    self.constraint_graph[var1].add(var2)  # Create a graph edge.

    def is_valid_assignment(self, assignment):
        """
        Checks whether a given assignment satisfies all constraints.
        - assignment: Dictionary mapping variables to assigned values.
        """
        for variables, constraint_fn in self.constraints:  # Iterate over all constraints.
            values = [assignment.get(var) for var in variables]  # Get the values assigned to these variables.
            if None not in values and not constraint_fn(*values):  # If all values are assigned but the constraint fails,
                return False  # Return false for invalid assignment.
        return True  # All constraints are satisfied.

    def get_neighbors(self, var):
        """
        Retrieves neighbors of a variable from the constraint graph.
        """
        return self.constraint_graph.get(var, set())  # Return all connected variables.

    def display_constraint_graph_size(self):
        """
        Displays the size of the constraint graph.
        - Nodes: Number of variables.
        - Edges: Number of unique edges (constraints).
        """
        num_nodes = len(self.variables)  # Count nodes in the graph.
        num_edges = sum(len(neighbors) for neighbors in self.constraint_graph.values()) // 2  # Count unique edges.
        print(f"Constraint Graph: {num_nodes} nodes, {num_edges} edges")  # Display graph size.
