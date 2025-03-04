# Kakuro Puzzle Solver 

##  Problem Description  
This project focuses on solving **Kakuro puzzles**, a numerical crossword game, using **Constraint Satisfaction Problems (CSP)** techniques. The goal is to fill in blank cells ("?") with numbers from **1 to 9** while satisfying the following constraints:  

1️⃣ **Sum Constraint:** The sum of the numbers in each horizontal or vertical group must match the provided clue.  
2️⃣ **Uniqueness Constraint:** Numbers within a group must be distinct.  

The Kakuro board consists of:  
- **Clue Cells** – Indicate target sums for groups of blank cells (e.g., `"15/"` means a sum of 15 vertically).  
- **Variable Cells** – Blank cells ("?") to be filled with numbers from 1 to 9.  

---

## 🛠️ Approach & Methods  
The problem is represented as a **Constraint Satisfaction Problem (CSP)** with:  
- **Variables** → Each blank cell.  
- **Domains** → Possible values `[1-9]` for each cell.  
- **Constraints** → Sum and uniqueness constraints.  

### 🔹 **Algorithms Used:**  
✔ **Backtracking Search**  
✔ **AC-3 (Arc Consistency 3)**   
✔ **Forward Checking (FC)** 
✔ **Fail First Principle (FFP)**   
✔ **Dependency Directed Backtracking (DDB)**  

I test these techniques separately or combine them to determine the best approach for solving this game.
