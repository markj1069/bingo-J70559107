import random

class RandomUniqueGenerator:
    """
    Generates uniform random numbers from 1 to n without duplicates
    until all numbers are used, then can be reset.
    """
    
    def __init__(self, n: int):
        if n < 1:
            raise ValueError("n must be at least 1")
        self.n = n
        self._numbers = []
        self.reset()
    
    def get(self) -> int:
        """Returns the next unique random number. Raises StopIteration when exhausted."""
        if not self._numbers:
            raise StopIteration(f"All numbers from 1 to {self.n} have been used. Call reset() to start over.")
        
        return self._numbers.pop()
    
    def reset(self):
        """Reshuffle and reset the generator."""
        self._numbers = list(range(1, self.n + 1))
        random.shuffle(self._numbers)
    
    def remaining(self) -> int:
        """Returns how many numbers are left."""
        return len(self._numbers)
    
    def is_exhausted(self) -> bool:
        """Check if all numbers have been used."""
        return len(self._numbers) == 0


# ============================
# Example Usage
# ============================

if __name__ == "__main__":
    gen = RandomUniqueGenerator(10)
    
    print("Generating numbers 1-10 without duplicates:")
    for _ in range(10):
        print(gen.get(), end=" ")
    
    print(f"\nRemaining: {gen.remaining()}")
    
    # Try to get one more → will raise StopIteration
    # gen.get()
    
    print("\nResetting...")
    gen.reset()
    
    print("New sequence after reset:")
    for _ in range(5):
        print(gen.get(), end=" ")
