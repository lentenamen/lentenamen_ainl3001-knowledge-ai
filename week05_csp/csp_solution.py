"""
AINL3001 — Knowledge-Driven AI
Week 5 — Constraint Satisfaction Problems
BSP 2026

Australian map colouring: six regions and three colours.

Tasks
-----
0. Examine an invalid assignment.
1. Understand variables, domains and constraints.
2. Implement constraint checking.
3. Implement backtracking with simple variable selection.
4. Compare backtracking with brute force.
5. Improve variable selection using MRV.

Lecturer solution — release after the lab.
"""

# --------------------------------------------------
# TASK 0 — MANUAL EXPLORATION
# --------------------------------------------------

example_assignment = {
    "WA": "Red",
    "NT": "Red",
    "SA": "Green",
    "Q": "Blue",
    "NSW": "Red",
    "V": "Green",
}

print("Manual CSP Exploration")
print(example_assignment)
print("\nQuestions:")
print("1. Is this assignment valid?")
print("2. Which neighbouring pairs violate a constraint?")
print("3. How could you correct the assignment?")
print("4. Why is it useful to detect violations early?")
print("\nAnswer: WA–NT are both Red; SA–V are both Green.")

# --------------------------------------------------
# TASK 1 — CSP REPRESENTATION
# --------------------------------------------------

variables = ["WA", "NT", "SA", "Q", "NSW", "V"]

domains = {
    variable: ["Red", "Green", "Blue"]
    for variable in variables
}

constraints = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V"),
]

# --------------------------------------------------
# TASK 2 — CONSTRAINT CHECKING
# --------------------------------------------------

def is_valid_assignment(assignment):
    """Return True if a complete OR partial assignment is valid."""
    for region1, region2 in constraints:
        if region1 in assignment and region2 in assignment:
            if assignment[region1] == assignment[region2]:
                return False
    return True


# --------------------------------------------------
# TASK 3 AND TASK 5 — VARIABLE SELECTION
# --------------------------------------------------

def select_unassigned_variable(assignment):
    """Choose the next unassigned region using MRV (Task 5)."""
    # For Task 3, students first implement simple selection:
    #
    # for variable in variables:
    #     if variable not in assignment:
    #         return variable
    # return None
    #
    # Task 5 replaces that selection with MRV below.

    best_variable = None
    fewest_legal_colours = float("inf")

    for variable in variables:
        if variable in assignment:
            continue

        legal_colours = 0
        for colour in domains[variable]:
            assignment[variable] = colour
            if is_valid_assignment(assignment):
                legal_colours += 1
            del assignment[variable]

        if legal_colours < fewest_legal_colours:
            fewest_legal_colours = legal_colours
            best_variable = variable

    return best_variable


# --------------------------------------------------
# TASK 3 — BACKTRACKING SEARCH
# --------------------------------------------------

def backtracking_search(assignment):
    """Return a complete valid assignment, or None if none exists."""
    if len(assignment) == len(variables):
        return assignment.copy() if is_valid_assignment(assignment) else None

    variable = select_unassigned_variable(assignment)

    for colour in domains[variable]:
        assignment[variable] = colour

        if is_valid_assignment(assignment):
            result = backtracking_search(assignment)
            if result is not None:
                return result

        del assignment[variable]

    return None


# --------------------------------------------------
# TASK 4 — BRUTE FORCE COMPARISON
# --------------------------------------------------

# Six regions with three possible colours each give 3 ** 6 = 729
# complete assignments. Backtracking rejects invalid partial
# assignments, so it need not inspect all 729 complete assignments.


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("WEEK 5 — CONSTRAINT SATISFACTION PROBLEMS")
    print("=" * 50)

    print("\nVariables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)

    print("\nExample assignment valid?")
    print(is_valid_assignment(example_assignment))  # Expected: False

    partial_assignment = {"WA": "Red", "NT": "Green"}
    print("\nPartial assignment valid?")
    print(is_valid_assignment(partial_assignment))  # Expected: True

    print("\nSearching for a solution...")
    solution = backtracking_search({})
    print("Solution:", solution)

    if solution is not None:
        print("\nSolution valid?", is_valid_assignment(solution))
        print("\nColour assignment:")
        for region in variables:
            print(f"{region:4} -> {solution[region]}")
    else:
        print("No solution yet. Complete the TODO sections.")

    print("\nPossible complete assignments:", 3 ** len(variables))
    
    print("The result is valid, but it is not necessarily the only valid solution. Backtracking stops as soon as it finds one.")
    print(3 ** len(variables), " is the number of possible complete assignments, not the number the backtracking algorithm actually explored. Many of these might contain violations.")
    print("This number gives you a baseline for Task 4: Brute Force Comparison.")
    print("\nReflection:")
    print("1. What causes backtracking?")
    print("Backtracking occurs when an attempted assignment cannot lead to a valid solution. The algorithm removes the most recent assignment and tries another value.")
    print("2. Why can backtracking be faster than brute force?")
    print("Brute force could generate all possible complete assignments and then check whether each is valid.")
    print("3. Why might MRV reduce search?")
    print("It chooses the unassigned variable with the fewest currently legal values remaining.")
    print("4. How could this model represent timetabling?")
    print("We can use the same three CSP components such as variables, domains and constraints, to represent a timetabling problem.")
    print("variables: Lectures or classes")
    print("domains: Available room and time-slot combinations")
    print("constraints: Classes cannot clash in rooms, times or lecturer availability")
