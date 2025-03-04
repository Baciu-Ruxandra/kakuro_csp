from kakuro_solver import KakuroSolver


def main():
    # Define the Kakuro puzzle board as a 2D list.
    #6X6 (18 nec) -> SOLUTION
    board = [
        [None, "7/","13/","16/",None,None],
        ["/10","?","?","?","29/",None],
        ["/28", "?","?","?","?","6/"],
        ["/4","?","?","4/12","?","?"],
        [None, "/11", "?","?","?","?"],
        [None,None,"/10","?","?","?"],
    ]

    #6X6 (24 nec) -> NO solution
    board0 = [
        [None, "15/","13/","5/","22/","4/"],
        ["/5", "?","?","?","?","?"],
        ["/8", "?", "?", "?", "?", "?"],
        ["/4", "?", "?", "5/1", "?", "?"],
        ["/17", "?", "?", "?", "?", "?"],
        ["/29", "?", "?", "?", "?", "?"],
    ]

    #6X6(21 nec) -> SOLUTION found in 1 min
    board1 = [
        [None,"6/","26/",None,"31/","12/"],
        ["/8","?","?","12/9","?","?"],
        ["/30", "?", "?", "?", "?", "?"],
        [None, "9/17","?","?","?","16/"],
        ["/35","?", "?", "?", "?", "?"],
        ["/4", "?", "?", "/9", "?", "?"],
    ]


    #7X7 (16 nec)->SOLUTION
    board2 = [
        [None, None, "16/", "7/", None, None, None],
        [None, "5/14", "?", "?", "27/", None, None],
        ["/14", "?", "?", "?", "?", "11/", None],
        ["/4", "?", "?", "3/16", "?", "?", None],
        [None, "/17", "?", "?", "?", "?", None],
        [None, None, "/4", "?", "?", None, None],
        [None, None, None, None,None, None, None],
    ]

    #8X8 (29 nec)->SOLUTION
    board3 = [
        [None, "10/", "7/",None, "16/", "6/", None, None],
        ["/4", "?","?","/4","?","?","27/","8/"],
        ["/9", "?","?","20/29","?","?","?","?"],
        [None, "/10", "?","?","?","10/9","?","?"],
        [None, None, "8/10","?", "?", "?", "?",None],
        [None, "/5","?", "?","9/10","?", "?",None],
        [None, "/28","?", "?", "?", "?",None,None],
        [None, None, None,"/3","?", "?",None,None],
    ]

    #9X9(44 nec) SOLUTION
    board4 = [
        [None, None, "10/", "6/", None, None, "11/", "7/", None],
        [None, "/4", "?", "?", "11/", "/6", "?", "?", "3/"],
        [None, "3/8", "?", "?", "?", "/6", "?", "?", "?"],
        ["/10", "?", "?", "?", "?", "10/7", "?", "?", "?"],
        ["/3", "?", "?", "17/6", "?", "?", "?", "15/", "4/"],
        [None, "16/", "23/6", "?", "?", "?", "6/3", "?", "?"],
        ["/24", "?", "?", "?", "/10", "?", "?", "?", "?"],
        ["/23", "?", "?", "?", "/6", "?", "?", "?", None],
        [None, "/8", "?", "?", None, "/12", "?", "?", None],
    ]



    solver = KakuroSolver(board2)  # Create a solver instance.
    solver.parse_board()  # Parse the board into CSP variables and constraints.

    # Define combinations of methods to test.
    methods_combinations = {
        "Baseline Backtracking": {},
        "Backtracking + Forward Checking": {"Forward Checking": True},
        "Backtracking + AC-3": {"AC-3": True},
        "Backtracking + FFP": {"FFP": True},
        "Backtracking + DDB": {"DDB": True},
        "Backtracking + Forward Checking + FFP": {"Forward Checking": True, "FFP": True},
        "Backtracking + Forward Checking + DDB": {"Forward Checking": True, "DDB": True},
        "Backtracking + Forward Checking + AC-3 + FFP": {"Forward Checking": True, "AC-3": True, "FFP": True},
        "Backtracking + Forward Checking + AC-3 + DDB": {"Forward Checking": True, "AC-3": True, "DDB": True},
    }

    for name, methods in methods_combinations.items():  # Test each method combination.
        print(f"\nMethod: {name}")
        solution = solver.solve_with_methods(methods)  # Solve using the specified methods.
        solver.display_metrics()  # Display metrics.
        if solution:  # If a solution is found,
            print("Solution Found:")
            for r in range(len(board2)):  # Format and print the solution.
                row = []
                for c in range(len(board2[r])):
                    if (r, c) in solution:
                        row.append(solution[(r, c)])
                    else:
                        row.append(board2[r][c])
                print(row)
        else:
            print("No solution exists.")  # Print if no solution is found.

if __name__ == "__main__":
    main()  # Run the main function.
