import unittest
# from towers_of_power import compare_towers
# from simple_tower_of_power import compare_towers
from safe_tower_of_power import compare_towers

class TestTowerPowers(unittest.TestCase):
    def test_simple_numbers(self):
        """Test comparison of simple single numbers"""
        self.assertLess(compare_towers([15], [16]), 0)
        self.assertEqual(compare_towers([15], [15]), 0)
        self.assertGreater(compare_towers([16], [15]), 0)
    
    def test_empty_and_ones(self):
        """Test handling of empty lists and lists containing only 1s"""
        self.assertEqual(compare_towers([], []), 0)
        self.assertEqual(compare_towers([1], [1]), 0)
        self.assertEqual(compare_towers([1, 1], [1]), 0)
        self.assertEqual(compare_towers([1, 1, 1], [1, 1]), 0)
    
    def test_two_level_towers(self):
        """Test comparison of two-level towers"""
        self.assertLess(compare_towers([2, 3], [2, 4]), 0)  # 2^3 vs 2^4
        self.assertLess(compare_towers([2, 3], [3, 2]), 0)  # 2^3 vs 3^2
        self.assertEqual(compare_towers([2, 3], [2, 3]), 0)  # 2^3 vs 2^3
    
    def test_three_level_towers(self):
        """Test comparison of three-level towers"""
        self.assertLess(compare_towers([2, 2, 2], [2, 2, 3]), 0)  # 2^2^2 vs 2^2^3
        self.assertEqual(compare_towers([2, 2, 2], [2, 2, 2]), 0)  # 2^2^2 vs 2^2^2
    
    def test_different_lengths(self):
        """Test comparison of towers with different lengths"""
        self.assertLess(compare_towers([2], [2, 2]), 0)  # 2 vs 2^2
        self.assertLess(compare_towers([2, 2], [2, 2, 2]), 0)  # 2^2 vs 2^2^2
    
    def test_tricky_cases(self):
        """Test some tricky comparisons where intuition might fail"""
        # The case you pointed out:
        self.assertLess(compare_towers([100, 2, 3], [2, 100, 3]), 0)  # 100^2^3 vs 2^100^3
        
        # Some other interesting cases:
        self.assertEqual(compare_towers([2, 4], [4, 2]), 0)  # 2^4 vs 4^2
        self.assertLess(compare_towers([3, 2, 2], [2, 3, 2]), 0)  # 2^3^2 vs 3^2^2
    
    def test_large_values(self):
        """Test with values close to constraints"""
        self.assertLess(compare_towers([100], [100, 100]), 0)  # 100 vs 100^100
        self.assertLess(
            compare_towers([100] * 50, [100] * 51), 0
        )  # Tower of 50 100s vs Tower of 51 100s
    
    def test_base_cases_for_recursion(self):
        """Test cases that hit the base cases in the recursive logic"""
        # Test transitions around length 3 (where we switch to loglog comparison)
        self.assertLess(compare_towers([2, 2, 2], [2, 2, 3]), 0)
        self.assertLess(compare_towers([2, 2, 2, 2], [2, 2, 3, 2]), 0)

    def test_tricky_tower_comparisons(self):
        """Test cases with very subtle differences in towers"""
        
        # Same length towers with one small difference
        self.assertLess(
            compare_towers([100] * 49 + [99] + [100], [100] * 51),
            0
        )  # 50-length tower with one 99 vs all 100s
        
        # Different position of the smaller number
        self.assertGreater(
            compare_towers([100] * 25 + [99] + [100] * 25, [100] * 25 + [100] + [99] * 25),
            0
        )  # Where the 99 appears matters
        
        # One tower slightly larger in middle vs end
        self.assertLess(
            compare_towers([100] * 25 + [101] + [100] * 25, [100] * 50 + [102]),
            0
        )  # Extra large value in middle vs end
        
        # Comparing towers with alternating values
        self.assertLess(
            compare_towers([100, 99] * 25, [99, 100] * 25),
            0
        )  # 50-length towers with alternating values
        
        # Small difference at critical position
        self.assertGreater(
            compare_towers([2] + [100] * 49, [3] + [99] * 49),
            0
        )  # Different bases with almost max exponents
        
        # Testing boundary of our length <= 3 base case
        self.assertLess(
            compare_towers([100, 100, 99, 100], [100, 99, 100, 100]),
            0
        )  # 4-length towers with one 99 in different positions
        
        # Testing if position of larger number matters
        self.assertLess(
            compare_towers([100] * 24 + [101] + [100] * 25, [100] * 25 + [101] + [100] * 24),
            0
        )  # 50-length towers with one 101 in different positions
        
        # Testing cascading effect of small differences
        self.assertGreater(
            compare_towers([99] + [100] * 49, [100] + [99] * 49),
            0
        )  # Small difference at start vs small differences later
        
        # Testing effect of multiple small differences
        self.assertLess(
            compare_towers([100] * 25 + [99, 99] + [100] * 23, [100] * 25 + [99] + [100] * 24),
            0
        )  # Two adjacent 99s vs one 99
        
        # Testing sensitivity to position of differences
        self.assertGreater(
            compare_towers([2] + [100] * 48 + [3], [3] + [100] * 48 + [2]),
            0
        )  # Small numbers at opposite ends

    def test_tricky_heights(self):
        """Test tricky cases with tower heights"""
        self.assertLess(compare_towers([2] * 4, [99] * 3), 0)
        self.assertLess(compare_towers([2] * 5, [99] * 3), 0)
        self.assertGreater(compare_towers([2] * 6, [99] * 3), 0)
        
        self.assertGreater(compare_towers([2, 2, 2, 100], [100] * 3), 0)
        self.assertLess(compare_towers([2] * 5, [3, 3, 16]), 0)

if __name__ == '__main__':
    unittest.main()
    # print(compare_towers([2] * 5, [99] * 3))