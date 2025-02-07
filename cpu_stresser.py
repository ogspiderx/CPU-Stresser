import multiprocessing
import os
import random
import sys

if sys.platform == "win32":
    import tkinter as tk
    from tkinter import messagebox

def stress_cpu():
    """Function to stress CPU by performing heavy calculations."""
    while True:
        _ = sum(random.random() ** 2 for _ in range(10**6))

def stress_memory():
    """Function to stress memory by continuously allocating more memory."""
    memory_hog = []
    while True:
        memory_hog.extend(bytearray(10**7) for _ in range(10)) 

def confirm_run():
    """Display a confirmation prompt before starting the stress test."""
    if sys.platform == "win32":
        root = tk.Tk()
        root.withdraw()
        return messagebox.askyesno("Confirmation", "Are you sure you want to run the the CPU-Stresser? It may crash your device.")
    else:
        return input("Are you sure you want to run the the CPU-Stresser? It may crash your device. (yes/no): ").strip().lower() == "yes"

def main():
    if not confirm_run():
        return
    
    cpu_cores = os.cpu_count() or 4 
    processes = []
    
    for _ in range(cpu_cores):
        p = multiprocessing.Process(target=stress_cpu)
        p.start()
        processes.append(p)
    mem_process = multiprocessing.Process(target=stress_memory)
    mem_process.start()
    processes.append(mem_process)
    
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()
