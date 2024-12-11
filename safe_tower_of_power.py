import math
from functools import cmp_to_key

# Helper function for comparing log log of a small tower
# Assumes the tower has height <= 3
def loglog(x):
    assert len(x) <= 3
    if len(x) == 1:
        return math.log2(math.log2(x[0]))
    if len(x) == 2:
        return math.log2(math.log2(x[0])) + math.log2(x[1])
    if len(x) == 3:
        return math.log2(math.log2(x[0])) + math.log2(x[1]) * x[2]
    
# Helper function for comparing log of a small tower
# Assumes the tower has height <= 3
def log(x):
    assert len(x) <= 3
    if len(x) == 1:
        return math.log2(x[0])
    if len(x) == 2:
        return math.log2(x[0]) * x[1]
    if len(x) == 3:
        return math.log2(x[0]) * (x[1] ** x[2])
    
# Checks if it's safe to disregard the base of the tower
def _safe_compare(a, b, height=1):

    # Height = 1
    # Check if max(a, b) - log2(max(a, b)) - log2(log2(100)) > min(a, b) * log2(100) - log2(min(a, b))
    if height == 1:
        larger = max(a[-1], b[-1])
        smaller = min(a[-1], b[-1])
        if larger - math.log2(larger) - math.log2(math.log2(100)) > smaller * math.log2(100) - math.log2(smaller):
            return a[-1] - b[-1]
        else:
            # Not enough information to disregard the base
            return None
        
    # Height = 2
    # Check if log2(min(a, b)) + log2(2^delta - log2(100)) > log2(log2(max(a, b)) - log2(min(a, b)) + log2(log2(100)))
    elif height == 2:
        larger = log(a[-2:]) # log2(a[-2]) * a[-1]
        smaller = log(b[-2:])
        # First, compute delta, the difference between log2(a) and log2(b)
        delta = larger - smaller
        # Heuristic: if |delta| > 10, we can ignore an additive log2(100) term
        if abs(delta) < 10:
            delta = math.log2(2**delta - math.log2(100))
        if smaller + delta > math.log2(larger - smaller + math.log2(math.log2(100))):
            return log(a[-2:]) - log(b[-2:])
        else:
            return None
        
    # Height >= 3: unclear.
        
# Directly evaluate the top of a tower, length <= 3
def _eval_top(x):
    if len(x) == 0:
        return 1
    if len(x) == 1:
        return x[0]
    if len(x) == 2:
        return x[0] ** x[1]
    if len(x) == 3:
        return x[0] ** (x[1] ** x[2])

# Compare two numbers of the form a_1^a_2^...^a_n and b_1^b_2^...^b_n
# a, b are lists of integers in [1 ... 100] and n is in [1 ... 100]
def compare_towers(a, b):
    # Remove all 1s from the lists
    a = [x for x in a if x != 1]
    b = [x for x in b if x != 1]

    # If the first elements are the same, remove them
    while a and b and a[0] == b[0]:
        a.pop(0)
        b.pop(0)

    # If both lists are empty, the numbers are equal
    if not a and not b:
        return 0
    # If one list is empty, the other number is bigger
    if not a:
        return -1
    if not b:
        return 1
    
    # If the lists are of length <= 3, compare them directly
    if len(a) <= 3 and len(b) <= 3:
        return loglog(a) - loglog(b)
    
    height_gap = abs(len(a) - len(b))
    # Claim: if the difference in length of lists is >= 3, the longer list is bigger.
    if height_gap >= 3:
        return len(a) - len(b)
    
    # Now compare the ends of the lists, with the gap in mind
    i = max(len(a), len(b)) - 3
    a_top = a[i:] # length <= 3
    b_top = b[i:] # length <= 3

    # Compare: height = 1
    compare_height_1 = _safe_compare(a_top, b_top, height=1)
    if compare_height_1 is not None and compare_height_1 != 0:
        return compare_height_1
    
    # Compare: height = 2
    compare_height_2 = _safe_compare(a_top, b_top, height=2)
    if compare_height_2 is not None and compare_height_2 != 0:
        return compare_height_2
    
    # If we're here, means that the comparison is inconclusive but the tops are small. Let's just evaluate them and recurse.
    if compare_height_1 == 0 and compare_height_2 == 0:
        # Loop through the lists until we find a difference
        for j in range(i, -1, -1):
            if a[j] != b[j]:
                return a[j] - b[j]
        # If no difference is found, the numbers are equal
        return 0

    # pop the last two values from a and b and evaluate their powers
    a_highest_power, b_highest_power = _eval_top(a_top[1:]), _eval_top(b_top[1:])
    a = a[:i+1] + [a_highest_power]
    b = b[:i+1] + [b_highest_power]
    return compare_towers(a, b)


# Helper functions for testing
# ----------------------------

# Input parsing functions
def parse_tower_string(s: str) -> list:
    """Convert a string like '2^2^2' into a list [2,2,2]"""
    return [int(x) for x in s.split('^')]

def compare_tower_strings(a: str, b: str) -> int:
    """Compare two tower strings, maintaining stable sort"""
    return compare_towers(parse_tower_string(a), parse_tower_string(b))

def solve_tower_powers(numbers: list) -> list:
    """Sort the list of tower strings while maintaining original order for equal values"""
    # Create pairs of (index, number) to maintain original order
    indexed_numbers = list(enumerate(numbers))
    
    def compare_with_index(a, b):
        # Compare numbers first
        comp = compare_tower_strings(a[1], b[1])
        # If equal, maintain original order using index
        if comp == 0:
            return -1 if a[0] < b[0] else 1
        return comp
    
    # Sort using our custom comparator
    sorted_pairs = sorted(indexed_numbers, key=cmp_to_key(compare_with_index))
    
    # Extract just the numbers in sorted order
    return [num for _, num in sorted_pairs]

def main():
    # Read number of test cases
    M = int(input())
    numbers = []
    
    # Read each tower
    for _ in range(M):
        numbers.append(input().strip())
    
    # Sort and output
    print("Case 1:")
    sorted_numbers = solve_tower_powers(numbers)
    for num in sorted_numbers:
        print(num)

if __name__ == "__main__":
    main()