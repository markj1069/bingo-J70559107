import pytest
import random
from collections import Counter

from random_unique import RandomUniqueGenerator  # adjust import as needed


class TestRandomUniqueGenerator:

    def test_init_valid(self):
        gen = RandomUniqueGenerator(5)
        assert gen.n == 5
        assert gen.remaining() == 5
        assert not gen.is_exhausted()

    def test_init_invalid(self):
        with pytest.raises(ValueError):
            RandomUniqueGenerator(0)
        with pytest.raises(ValueError):
            RandomUniqueGenerator(-1)

    def test_get_returns_valid_numbers(self):
        gen = RandomUniqueGenerator(10)
        numbers = [gen.get() for _ in range(10)]
        
        assert len(numbers) == 10
        assert set(numbers) == set(range(1, 11))          # All numbers 1..10
        assert len(set(numbers)) == 10                    # No duplicates

    def test_no_duplicates_until_exhausted(self):
        gen = RandomUniqueGenerator(8)
        seen = set()
        
        for _ in range(8):
            num = gen.get()
            assert num not in seen
            seen.add(num)
        
        assert len(seen) == 8

    def test_exhaustion_raises_stopiteration(self):
        gen = RandomUniqueGenerator(3)
        for _ in range(3):
            gen.get()
        
        assert gen.is_exhausted()
        assert gen.remaining() == 0
        
        with pytest.raises(StopIteration):
            gen.get()

    def test_reset(self):
        gen = RandomUniqueGenerator(10)
        first_sequence = [gen.get() for _ in range(10)]
        
        gen.reset()
        second_sequence = [gen.get() for _ in range(10)]
        
        assert first_sequence != second_sequence   # Very likely different order
        assert set(first_sequence) == set(second_sequence)

    def test_multiple_resets(self):
        gen = RandomUniqueGenerator(5)
        sequences = []
        
        for _ in range(3):
            seq = [gen.get() for _ in range(5)]
            sequences.append(seq)
            gen.reset()
        
        # All sequences should contain same numbers but not be identical
        assert all(set(seq) == set(range(1, 6)) for seq in sequences)

    def test_remaining_counter(self):
        gen = RandomUniqueGenerator(7)
        assert gen.remaining() == 7
        
        for i in range(4):
            gen.get()
            assert gen.remaining() == 7 - (i + 1)

    def test_n_equal_to_one(self):
        gen = RandomUniqueGenerator(1)
        assert gen.get() == 1
        assert gen.is_exhausted()
        
        gen.reset()
        assert gen.get() == 1

    @pytest.mark.slow
    def test_uniform_distribution(self):
        """Statistical test - may occasionally fail due to randomness."""
        gen = RandomUniqueGenerator(10)
        trials = 1000
        counts = Counter()
        
        for _ in range(trials):
            gen.reset()
            counts[gen.get()] += 1   # Check first number distribution
        
        # Each number should appear roughly equally often
        expected = trials / 10
        for i in range(1, 11):
            assert expected * 0.7 < counts[i] < expected * 1.3   # Loose bounds

    def test_different_instances_independent(self):
        gen1 = RandomUniqueGenerator(5)
        gen2 = RandomUniqueGenerator(5)
        
        seq1 = [gen1.get() for _ in range(5)]
        seq2 = [gen2.get() for _ in range(5)]
        
        # They can be same by chance, but we just check they both work correctly
        assert set(seq1) == set(range(1, 6))
        assert set(seq2) == set(range(1, 6))
