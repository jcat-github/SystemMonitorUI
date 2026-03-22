import sys
import time
import psutil
import shutil

# Clear screen once
sys.stdout.write("\033[2J\033[H")
sys.stdout.flush()

while True:
    # Get CPU percentages
    cpu_percents = psutil.cpu_percent(interval=0.5, percpu=True)
    num_cores = len(cpu_percents)

    # Move cursor to start of block (top-left)
    sys.stdout.write("\033[H")

    # Write each CPU core on its own line
    for i, perc in enumerate(cpu_percents):
        line = f"CPU {i}: {perc:3}%"
        # Pad to full width (optional)
        sys.stdout.write(line + "\n")

    sys.stdout.flush()

    # Wait before next update
    time.sleep(0.5)