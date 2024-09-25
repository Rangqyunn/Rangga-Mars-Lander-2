import sys

MAX_VH = 20  # Maximum safe horizontal speed

# Find a flat landing zone
def find_landing_zone(surface):
    for i in range(1, len(surface)):
        if surface[i - 1][1] == surface[i][1]:  # Look for two consecutive points with the same height
            return (i - 1, i)
    return (0, 0)

# Load program for easy landing to the right
def load_easy_right():
    print("easy landing to the right", file=sys.stderr, flush=True)
    program = [(-30, 4)] * 11  # Decelerate first
    program += [(0, 4), (0, 3)] * 999  # Stabilize descent
    return program

# Load program for landing with high horizontal speed to the left
def load_left_too_fast():
    print("high horizontal speed landing to the left", file=sys.stderr, flush=True)
    program = [(-40, 4)] * 42  # Decelerate horizontally
    program += [(0, 4)] * 15  # Stabilize
    program += [(0, 4), (0, 3)] * 999  # Controlled descent
    return program

# Load program for landing with high horizontal speed and short distance to the left
def load_left_too_fast_too_close():
    print("high horizontal speed landing little to the left, just below", file=sys.stderr, flush=True)
    program = [(-50, 4)] * 38  # Steeper deceleration
    program += [(0, 4)] * 32  # Slow down and stabilize
    program += [(0, 4), (0, 3)] * 999
    return program

# Load program for landing in a deep canyon on the far right
def load_deep_canyon_far_right():
    print("deep canyon landing on the far right", file=sys.stderr, flush=True)
    program = [(32, 4)] * 52  # Move horizontally to the right
    program += [(0, 4), (0, 3)] * 999  # Controlled descent
    return program

# Load program for landing on high ground on the far left
def load_high_ground_landing():
    print("landing on high ground on far left", file=sys.stderr, flush=True)
    program = [(0, 4), (0, 4), (0, 4), (0, 3)] * 12  # Slow, steady descent
    program += [(-12, 4)] * 52  # Adjust horizontal position
    program += [(0, 4), (0, 3)] * 99  # Final descent
    return program

# Check if close to a mountain peak
def is_near_mountain_peak(x, y, surface):
    if y < 1000:
        return False
    for x_s, y_s in surface:
        dist = abs(x - x_s) + abs(y - y_s)
        if dist < 1000:  # If near a peak
            return True
    return False

# Determine which program to load based on current position and speed
def load_program(x, y, h_speed, v_speed, surface):
    landing_begin, landing_end = find_landing_zone(surface)
    lz_begin = surface[landing_begin]
    lz_end = surface[landing_end]

    if x < lz_begin[0]:
        if is_near_mountain_peak(x, y, surface):
            return load_deep_canyon_far_right()  # Move right if close to a mountain peak
        return load_easy_right()
    elif h_speed < -MAX_VH and x > lz_end[0]:
        if lz_end[1] > 2000:  # High ground landing
            return load_high_ground_landing()
        if abs(x - lz_end[0]) > 2000:  # Adjust for fast horizontal speed
            return load_left_too_fast()
        return load_left_too_fast_too_close()

    return [(0, 0)] * 999  # Default to stable descent

# Parse input and create the surface
surface_n = int(input())  # Number of points defining the surface
surface = []
for i in range(surface_n):
    land_x, land_y = map(int, input().split())  # Coordinates of the surface
    surface.append((land_x, land_y))

# Variables to track program execution
program = []
program_i = 0

# Main game loop
while True:
    # Read the current state of the lander
    x, y, h_speed, v_speed, fuel, rotate, power = map(int, input().split())

    # Load a program if we don't have one
    if len(program) == 0:
        program = load_program(x, y, h_speed, v_speed, surface)

    # Execute the next step in the program
    out_rotate, out_power = program[program_i]
    print(out_rotate, out_power)

    # Increment program counter
    program_i += 1
