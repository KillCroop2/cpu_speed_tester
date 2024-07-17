import time
import math
import multiprocessing
import psutil

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def find_primes(start, end):
    return [num for num in range(start, end) if is_prime(num)]

def single_thread_test(range_start, range_end):
    start_time = time.time()
    primes = find_primes(range_start, range_end)
    end_time = time.time()
    return end_time - start_time

def multi_thread_test(range_start, range_end, num_processes):
    chunk_size = (range_end - range_start) // num_processes
    chunks = [(range_start + i * chunk_size, range_start + (i + 1) * chunk_size) for i in range(num_processes)]
    
    start_time = time.time()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(find_primes, chunks)
    end_time = time.time()
    
    return end_time - start_time

if __name__ == "__main__":
    range_start = 2
    range_end = 1000000
    
    print("CPU Speed Test")
    print(f"Testing range: {range_start} to {range_end}")
    
    # Single-thread test
    single_thread_time = single_thread_test(range_start, range_end)
    print(f"Single-thread time: {single_thread_time:.2f} seconds")
    
    # Multi-thread test
    num_cores = psutil.cpu_count(logical=False)
    num_threads = psutil.cpu_count(logical=True)
    print(f"\nNumber of physical cores: {num_cores}")
    print(f"Number of logical cores (threads): {num_threads}")
    
    multi_thread_time = multi_thread_test(range_start, range_end, num_threads)
    print(f"Multi-thread time: {multi_thread_time:.2f} seconds")
    
    # Calculate speedup
    speedup = single_thread_time / multi_thread_time
    print(f"\nSpeedup: {speedup:.2f}x")
    print(f"Efficiency: {speedup / num_threads:.2f}")
