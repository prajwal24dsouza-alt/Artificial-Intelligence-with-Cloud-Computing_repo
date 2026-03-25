"""
Comparison: Python Lists vs NumPy Arrays with 1 Million Numbers
================================================================
This script benchmarks common operations on Python lists and NumPy arrays
to demonstrate the performance differences between them.
"""

import time
import numpy as np

SIZE = 1_000_000  # 1 million elements

def measure_time(func):
    """Measure execution time of a function."""
    start = time.time()
    result = func()
    end = time.time()
    return result, end - start

print("=" * 65)
print("  Python Lists vs NumPy Arrays — Performance Comparison")
print(f"  Dataset size: {SIZE:,} numbers")
print("=" * 65)

# ──────────────────────────────────────────────────────────────
# 1. CREATION
# ──────────────────────────────────────────────────────────────
print("\n 1. Creation Time")

_, list_create_time = measure_time(lambda: list(range(SIZE)))
_, np_create_time = measure_time(lambda: np.arange(SIZE))

print(f"   Python List : {list_create_time:.6f} seconds")
print(f"   NumPy Array : {np_create_time:.6f} seconds")
print(f"   ⚡ NumPy is {list_create_time / np_create_time:.1f}x faster")

# Create the data for subsequent tests
python_list = list(range(SIZE))
numpy_array = np.arange(SIZE)

# ──────────────────────────────────────────────────────────────
# 2. ELEMENT-WISE ADDITION (each element + 5)
# ──────────────────────────────────────────────────────────────
print("\n 2. Element-wise Addition (each element + 5)")

_, list_add_time = measure_time(lambda: [x + 5 for x in python_list])
_, np_add_time = measure_time(lambda: numpy_array + 5)

print(f"   Python List : {list_add_time:.6f} seconds")
print(f"   NumPy Array : {np_add_time:.6f} seconds")
print(f"   ⚡ NumPy is {list_add_time / np_add_time:.1f}x faster")

# ──────────────────────────────────────────────────────────────
# 3. ELEMENT-WISE MULTIPLICATION (each element × 2)
# ──────────────────────────────────────────────────────────────
print("\n 3. Element-wise Multiplication (each element × 2)")

_, list_mul_time = measure_time(lambda: [x * 2 for x in python_list])
_, np_mul_time = measure_time(lambda: numpy_array * 2)

print(f"   Python List : {list_mul_time:.6f} seconds")
print(f"   NumPy Array : {np_mul_time:.6f} seconds")
print(f"   ⚡ NumPy is {list_mul_time / np_mul_time:.1f}x faster")

# ──────────────────────────────────────────────────────────────
# 4. SUM OF ALL ELEMENTS
# ──────────────────────────────────────────────────────────────
print("\n 4. Sum of All Elements")

list_sum, list_sum_time = measure_time(lambda: sum(python_list))
np_sum, np_sum_time = measure_time(lambda: np.sum(numpy_array))

print(f"   Python List : {list_sum_time:.6f} seconds  (sum = {list_sum})")
print(f"   NumPy Array : {np_sum_time:.6f} seconds  (sum = {np_sum})")
print(f"   ⚡ NumPy is {list_sum_time / np_sum_time:.1f}x faster")

# ──────────────────────────────────────────────────────────────
# 5. DOT PRODUCT (element-wise multiply + sum)
# ──────────────────────────────────────────────────────────────
print("\n 5. Dot Product")

list_b = list(range(SIZE))
np_b = np.arange(SIZE)

_, list_dot_time = measure_time(
    lambda: sum(a * b for a, b in zip(python_list, list_b))
)
_, np_dot_time = measure_time(lambda: np.dot(numpy_array, np_b))

print(f"   Python List : {list_dot_time:.6f} seconds")
print(f"   NumPy Array : {np_dot_time:.6f} seconds")
print(f"   ⚡ NumPy is {list_dot_time / np_dot_time:.1f}x faster")

# ──────────────────────────────────────────────────────────────
# 6. MEMORY USAGE
# ──────────────────────────────────────────────────────────────
import sys
print("\n 6. Memory Usage")

list_mem = sys.getsizeof(python_list) + sum(sys.getsizeof(x) for x in python_list[:100]) / 100 * SIZE
np_mem = numpy_array.nbytes

print(f"   Python List : ~{list_mem / (1024**2):.2f} MB")
print(f"   NumPy Array :  {np_mem / (1024**2):.2f} MB")
print(f"   NumPy uses ~{list_mem / np_mem:.1f}x less memory")

# ──────────────────────────────────────────────────────────────
# SUMMARY TABLE
# ──────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  SUMMARY TABLE")
print("=" * 65)
print(f"  {'Operation':<30} {'List (s)':>10} {'NumPy (s)':>10} {'Speedup':>8}")
print("  " + "-" * 61)
print(f"  {'Creation':<30} {list_create_time:>10.6f} {np_create_time:>10.6f} {list_create_time/np_create_time:>7.1f}x")
print(f"  {'Addition (+5)':<30} {list_add_time:>10.6f} {np_add_time:>10.6f} {list_add_time/np_add_time:>7.1f}x")
print(f"  {'Multiplication (×2)':<30} {list_mul_time:>10.6f} {np_mul_time:>10.6f} {list_mul_time/np_mul_time:>7.1f}x")
print(f"  {'Sum':<30} {list_sum_time:>10.6f} {np_sum_time:>10.6f} {list_sum_time/np_sum_time:>7.1f}x")
print(f"  {'Dot Product':<30} {list_dot_time:>10.6f} {np_dot_time:>10.6f} {list_dot_time/np_dot_time:>7.1f}x")

# ──────────────────────────────────────────────────────────────
# 3 KEY OBSERVATIONS
# ──────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  3 KEY OBSERVATIONS")
print("=" * 65)
print("""
  1. SPEED — NumPy arrays are dramatically faster (often 10-100x)
     for numerical operations because they use optimized C routines
     and vectorized operations, avoiding Python's per-element
     interpreter overhead.

  2. MEMORY EFFICIENCY — NumPy arrays store homogeneous data in
     contiguous memory blocks, requiring significantly less memory
     (~3-8x less) compared to Python lists, which store individual
     Python objects with extra type and reference-count overhead.

  3. VECTORIZATION — NumPy eliminates the need for explicit Python
     loops (list comprehensions / for-loops). Operations like
     `array + 5` or `np.dot()` are applied to the entire array at
     once, making code both faster AND more concise/readable.
""")
