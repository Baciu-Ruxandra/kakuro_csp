from csp import CSP  # Import the CSP class for constraint satisfaction functionality.
import time  # Used for performance measurement.

class KakuroSolver:
    def __init__(self, board):
        """
        Initializes the Kakuro solver with the given board.
        - board: The Kakuro puzzle board as a 2D list.
        """
        self.board = board  # Store the puzzle board.
        self.csp = CSP()  # Initialize an instance of CSP to manage variables and constraints.
        self.assignment_count = 0  # Track the number of assignments during solving.
        self.time_taken = 0  # Track the time taken to solve the puzzle.

    def parse_board(self):
        """
        Parses the board to extract variables and constraints into the CSP.
        """
        rows, cols = len(self.board), len(self.board[0])  # Dimensions of the board.

        def find_group(r, c, dr, dc):
            """
            Finds a group of cells (variables) starting from (r, c) in the direction (dr, dc).
            """
            group = []  # To store variables in the group.
            while 0 <= r < rows and 0 <= c < cols and self.board[r][c] == "?":  # Traverse until out of bounds or not a variable.
                group.append((r, c))  # Add the cell to the group.
                r += dr  # Move to the next cell in the direction.
                c += dc
            return group  # Return the group of variables.

        for r in range(rows):  # Loop through every row.
            for c in range(cols):  # Loop through every column.
                if isinstance(self.board[r][c], str) and "/" in self.board[r][c]:  # Check if the cell is a sum clue.
                    # Process horizontal groups.
                    if c + 1 < cols and self.board[r][c + 1] == "?":
                        h_group = find_group(r, c + 1, 0, 1)  # Get the horizontal group.
                        h_sum = int(self.board[r][c].split("/")[1])  # Extract the horizontal sum.
                        self.add_group_to_csp(h_group, h_sum)  # Add this group to the CSP.

                    # Process vertical groups.
                    if r + 1 < rows and self.board[r + 1][c] == "?":
                        v_group = find_group(r + 1, c, 1, 0)  # Get the vertical group.
                        v_sum = int(self.board[r][c].split("/")[0])  # Extract the vertical sum.
                        self.add_group_to_csp(v_group, v_sum)  # Add this group to the CSP.

    def add_group_to_csp(self, group, target_sum):
        """
        Adds a group of variables to the CSP with a constraint ensuring their sum matches the target_sum.
        - group: List of variables (cells) in the group.
        - target_sum: The required sum for the group.
        """
        for var in group:  # Add each variable in the group to the CSP.
            if var not in self.csp.variables:  # If the variable is not already in the CSP,
                self.csp.add_variable(var, list(range(1, 10)))  # Add it with a domain of [1-9].

        def sum_constraint(*values):
            """
            Constraint function for the group:
            - The sum of the values must equal the target sum.
            - All values must be unique.
            """
            return sum(values) == target_sum and len(values) == len(set(values))

        self.csp.add_constraint(group, sum_constraint)  # Add the sum constraint for the group.

    def forward_checking(self, assignment, var, value):
        """
        Perform forward checking after assigning a value to a variable.
        - assignment: Current partial assignment of variables.
        - var: The variable to which a value is being assigned.
        - value: The value being assigned.
        """
        pruned_domains = {}  # Track pruned domain values.
        for neighbor in self.csp.get_neighbors(var):  # Check all neighbors of the assigned variable.
            if neighbor not in assignment:  # If the neighbor is not yet assigned,
                pruned_domains[neighbor] = []  # Initialize pruned list for this neighbor.
                for neighbor_value in self.csp.variables[neighbor]:  # For each value in the neighbor's domain,
                    temp_assignment = assignment.copy()  # Create a temporary assignment.
                    temp_assignment[neighbor] = neighbor_value  # Assign the value temporarily.
                    if not self.csp.is_valid_assignment(temp_assignment):  # If it violates any constraint,
                        pruned_domains[neighbor].append(neighbor_value)  # Add the value to the pruned list.
                for pruned_value in pruned_domains[neighbor]:  # Remove all pruned values from the domain.
                    self.csp.variables[neighbor].remove(pruned_value)
        return pruned_domains  # Return the pruned domains.

    def restore_domains(self, pruned_domains):
        """
        Restores pruned domains after backtracking.
        - pruned_domains: A dictionary of pruned values for each variable.
        """
        for var, values in pruned_domains.items():  # For each variable with pruned values,
            self.csp.variables[var].extend(values)  # Restore the values to its domain.

    def ac3(self):
        """
        Applies the AC-3 algorithm to enforce arc-consistency for the CSP.
        """
        queue = [(Xi, Xj) for Xi in self.csp.variables for Xj in self.csp.get_neighbors(Xi)]  # Initialize the arc queue.
        while queue:  # Process arcs until the queue is empty.
            Xi, Xj = queue.pop(0)  # Get an arc from the queue.
            if self.revise(Xi, Xj):  # Revise the domain of Xi.
                if not self.csp.variables[Xi]:  # If Xi's domain is empty, return failure.
                    return False
                for Xk in self.csp.get_neighbors(Xi) - {Xj}:  # Add neighbors of Xi back to the queue.
                    queue.append((Xk, Xi))
        return True  # Arc-consistency enforced.

    def revise(self, Xi, Xj):
        """
        Revise the domain of Xi to ensure arc-consistency with Xj.
        - Xi: Variable whose domain is being revised.
        - Xj: Neighbor variable.
        """
        revised = False
        for x in self.csp.variables[Xi]:  # For each value in Xi's domain,
            if not any(self.csp.is_valid_assignment({Xi: x, Xj: y}) for y in self.csp.variables[Xj]):  # If no value in Xj's domain is consistent,
                self.csp.variables[Xi].remove(x)  # Remove x from Xi's domain.
                revised = True
        return revised  # Return whether the domain was revised.

    def select_variable_mrv(self, assignment):
        """
        Select the variable with the smallest domain (Minimum Remaining Values heuristic).
        - assignment: Current partial assignment of variables.
        """
        unassigned = [v for v in self.csp.variables if v not in assignment]  # Get all unassigned variables.
        return min(unassigned, key=lambda var: len(self.csp.variables[var]))  # Return the variable with the smallest domain.

    def dependency_directed_backtracking(self, assignment={}, conflict_set=None):
        """
        Implements Dependency Directed Backtracking (DDB) for the Kakuro solver.
        - assignment: Current partial assignment of variables.
        - conflict_set: Tracks conflicts for backjumping.
        """
        if conflict_set is None:  # Initialize the conflict set if not provided.
            conflict_set = {var: set() for var in self.csp.variables}

        if len(assignment) == len(self.csp.variables):  # If all variables are assigned,
            return assignment  # Return the complete assignment.

        var = next(v for v in self.csp.variables if v not in assignment)  # Select the first unassigned variable.

        for value in self.csp.variables[var]:  # Iterate over the variable's domain.
            assignment[var] = value  # Assign the value.
            self.assignment_count += 1  # Increment the assignment count.

            if self.csp.is_valid_assignment(assignment):  # Check if the assignment is valid.
                result = self.dependency_directed_backtracking(assignment,
                                                               conflict_set)  # Recurse with updated assignment.
                if result:  # If a solution is found,
                    return result  # Return it.

            del assignment[var]  # Backtrack by removing the assignment.

        # If no value works, update the conflict set for backjumping.
        for neighbor in self.csp.get_neighbors(var):  # Check all neighbors.
            if neighbor in assignment:  # If the neighbor is already assigned,
                conflict_set[neighbor].add(var)  # Add the current variable to its conflict set.

        # Backjump to the most recent variable in the conflict set.
        valid_conflicts = [v for v in conflict_set[var] if v in assignment]  # Only consider valid conflicts.
        if valid_conflicts:  # If there are valid conflicts,
            backjump_target = max(valid_conflicts, key=lambda v: list(assignment).index(v))  # Get the most recent one.
            del assignment[backjump_target]  # Remove it from the assignment.
        else:
            return None  # No valid backjump target; terminate.

        return None  # Return None if no solution is found.

    def backtracking_with_methods(self, assignment={}, methods=None):
        """
        General backtracking algorithm with optional methods, including DDB.
        - methods: Dictionary specifying which methods to use (e.g., forward checking, AC-3, DDB, FFP).
        """
        if len(assignment) == len(self.csp.variables):  # If all variables are assigned,
            return assignment  # Return the complete assignment.

        if methods and "DDB" in methods:  # Use Dependency Directed Backtracking if specified.
            return self.dependency_directed_backtracking(assignment)

        if methods and "AC-3" in methods:  # Apply AC-3 if specified.
            self.ac3()

        if methods and "FFP" in methods:  # Use Minimum Remaining Values (MRV) if FFP is specified.
            var = self.select_variable_mrv(assignment)
        else:  # Otherwise, select the first unassigned variable.
            var = next(v for v in self.csp.variables if v not in assignment)

        for value in self.csp.variables[var]:  # Iterate over the values in the variable's domain.
            assignment[var] = value  # Assign the value.
            self.assignment_count += 1  # Increment the assignment count.

            pruned_domains = {}
            if methods and "Forward Checking" in methods:  # Perform forward checking if specified.
                pruned_domains = self.forward_checking(assignment, var, value)

            if self.csp.is_valid_assignment(assignment):  # Check if the assignment is valid.
                result = self.backtracking_with_methods(assignment, methods)  # Recurse with the updated assignment.
                if result:  # If a solution is found,
                    return result

            del assignment[var]  # Backtrack by removing the variable's assignment.
            if methods and "Forward Checking" in methods:  # Restore domains if forward checking was used.
                self.restore_domains(pruned_domains)

        return None  # Return None if no solution is found.

    def solve_with_methods(self, methods=None):
        """
        Solve the Kakuro puzzle using backtracking with specified methods.
        """
        self.assignment_count = 0  # Reset the assignment count.
        start_time = time.time()  # Start timing.
        solution = self.backtracking_with_methods({}, methods)  # Solve using the specified methods.
        self.time_taken = time.time() - start_time  # Record the time taken to solve.
        return solution  # Return the solution.

    def display_metrics(self):
        """
        Displays performance metrics, including graph size, time taken, and assignments made.
        """
        self.csp.display_constraint_graph_size()  # Display the size of the constraint graph.
        print(f"Time Taken: {self.time_taken:.4f} seconds")  # Display the time taken.
        print(f"Assignments Made: {self.assignment_count}")  # Display the number of assignments made.
