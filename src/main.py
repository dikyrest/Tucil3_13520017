# main.py
# Contains main program including GUI

import tkinter as tk
import time
from puzzle import Puzzle
from prioQueue import PriorityQueue
from node import Node

# g(i) function for checking misplaced tiles
def check_misplaced_tiles(puzzle):
    result = 0
    flat = puzzle.flattened_board()
    
    for i in range(1, puzzle.n**2+1):
        if(flat[i-1] != i):
            result += 1

    return result

# Check whether matrix is sorted or not
def check_goal(puzzle):
    flat = puzzle.flattened_board()
    
    for i in range(1, (puzzle.n**2)+1):
        if(flat[i-1] != i):
            return False

    return True

# Generate solution from solved node
def generate_solution(solved_state):
    solution = []

    prev = solved_state
    state = solved_state.parent

    while(state != None):
       solution.insert(0, prev)
       prev = state
       state = state.parent
    
    return solution

# Display kurang(i) table
def display_table(table):
    lbl = tk.Label(master=kurang_frm, text="i")
    lbl.grid(row=0, column=0)
    lbl = tk.Label(master=kurang_frm, text="kurang(i)")
    lbl.grid(row=0, column=1)
    for i, kurang in enumerate(table):
        lbl = tk.Label(master=kurang_frm, text=i+1)
        lbl.grid(row=i+1, column=0)
        lbl = tk.Label(master=kurang_frm, text=kurang)
        lbl.grid(row=i+1, column=1)

# Clear puzzle frame
def clear_puzzle_frame():
    for widgets in puzzle_frm.winfo_children():
        widgets.destroy()

# Command for puzzle button to move empty cell
def puzzle_switch(btn):
    if (solution_array != None):
        if (len(solution_array)>0):
            num = btn["text"]
            move = solution_array[0].move
            idx = moves_names.index(move)
            (dr, dc) = moves_units[idx]
            sr = xypos['empty'][0]     # Position of 'empty'
            sc = xypos['empty'][1]
            r = xypos[num][0]          # Position of selected button
            c = xypos[num][1]

            # Is the selected button matches the move?
            if(r == sr + dr and c == sc + dc):
                # Swap button with empty
                xypos['empty'], xypos[num] = xypos[num], xypos['empty']

                # Re-position button
                btn.place(relx=xypos[num][1]/root.puzzle.n, rely=xypos[num][0]/root.puzzle.n)
                solution_array.pop(0)

                # Print if there are remaining moves
                if (len(solution_array) > 0):
                    move = solution_array[0].move
                    move_lbl["text"] = move
                else:
                    move_lbl["text"] = "Solved!"
        else:
            move_lbl["text"] = "Solved!"
    else:
        move_lbl["text"] = "---"

# Command fot solve button
def solve_button_clicked():
    global xypos, solution_array, root, moves_names, moves_units

    # Clear all buttons in puzzle frame
    clear_puzzle_frame()

    # Variable to store the solution
    solution_array = None

    # Get filename from user input
    filename = filename_entry.get()
    root = Node( Puzzle("../test/" + filename) )
    flat = root.puzzle.flattened_board()

    # Create dict of button positions and display puzzle
    xypos = {}
    xypos["empty"] = root.puzzle.find_empty()
    for i in range(root.puzzle.n):
        for j in range(root.puzzle.n):
            num = flat[i*root.puzzle.n + j]
            xypos[num] = (i, j)
            if (num != root.puzzle.n**2):
                num_btn = tk.Button(master=puzzle_frm, text=num, font=font_puzzle, fg="blue", width=4, height=2, bg="skyblue")
                num_btn["command"] = lambda num_btn=num_btn: puzzle_switch(num_btn)
                num_btn.place(relx=j/root.puzzle.n, rely=i/root.puzzle.n, relwidth=1/root.puzzle.n, relheight=1/root.puzzle.n)

    # Check if puzzle is solvable
    is_solveable, inversion, parity, total, kurang_i = root.puzzle.is_solveable()
    if (not is_solveable):
        solveable_lbl["text"] = "Puzzle is unsolvable."
        solveable_lbl["bg"] = "light salmon"
        display_table(kurang_i)
        verdict_lbl["text"] = "Inversions: " + str(inversion) + "\nParity: " + str(parity) + "\nTotal: " + str(total)
        move_lbl["text"] = "---"
        details_lbl["text"] = "---"
        return
    solveable_lbl["text"] = "Puzzle is solvable."
    solveable_lbl["bg"] = "light green"
    display_table(kurang_i)
    verdict_lbl["text"] = "Inversions: " + str(inversion) + "\nParity: " + str(parity) + "\nTotal: " + str(total)

    # Node generated count
    node_count = 1

    # Make priority queue for branching
    # On priority : lowest cost with last in first
    cost_function = check_misplaced_tiles
    pq = PriorityQueue(lambda x,y : x.depth + cost_function(x.puzzle) <= y.depth + cost_function(y.puzzle))

    # Initiate priority queue
    pq.push(root)

    # Variable to store solution state
    solution_state = None

    # List possible moves for puzzle
    moves_units = [(-1,0), (0,-1), (1,0), (0,1)]
    moves_names = ["Up", "Left", "Down", "Right"]

    # Start timer
    time_start = time.process_time_ns()

    # Searching for solution using Branch and Bound
    while(not pq.is_empty()):
        # Get front item in queue
        current = pq.front()
        pq.pop()

        # If currently checking final state, save the current state
        if (check_goal(current.puzzle)):
            solution_state = current
            break

        # Append generate states to pq
        for i, (dr, dc) in enumerate(moves_units):
            # If moves are NOT opposite to previous move, generate new node
            if(moves_names[(i+2)%4] != current.move):
                # Generate node
                result = Node(current.puzzle.move(dr, dc), parent=current, depth=current.depth+1, move=moves_names[i])

                # If move is possible..
                if(result != None and result.puzzle != None):
                    node_count += 1
                    pq.push( result )

    # Generate solution from result
    solution_array = generate_solution(solution_state)

    # Print the first move
    move = solution_array[0].move
    move_lbl["text"] = move

    # Stop timer
    time_stop = time.process_time_ns()

    time_taken = (time_stop - time_start) / 1000000
    details_lbl["text"] = "Total moves: " + str(len(solution_array)) + "\n" + str(node_count) + " nodes generated\n" + str(time_taken) + " ms taken"

# -=-=-=-=- MAIN PROGRAM -=-=-=-=- #

# Main window
window = tk.Tk()
window.title("15 PUZZLE SOLVER")

# Font list
font_title = ('Monaco', 20, 'bold')
font_label = ('Times', 12)
font_puzzle = ('Comic Sans MS', 12)

# Entry frame contains title, filename input, and solve button
entry_frm = tk.Frame(master=window, height=100, bg="gray80")
entry_frm.pack(fill=tk.X)
title_lbl = tk.Label(master=entry_frm, text="15 PUZZLE SOLVER", font=font_title, bg="gray80")
title_lbl.pack(pady=5)
filename_lbl = tk.Label(master=entry_frm, text="Enter the file name:", font=font_label, bg="gray80")
filename_lbl.pack(side=tk.LEFT)
filename_entry = tk.Entry(master=entry_frm, font=font_label, bg="white")
filename_entry.pack(pady=5, padx=10, side=tk.LEFT)
solve_btn = tk.Button(master=entry_frm, text="solve", font=font_label, bg="gray80", command=solve_button_clicked)
solve_btn.pack(pady=5, side=tk.LEFT)

# Center frame contains puzzle, move, and details
center_frm = tk.Frame(master=window, height=250, width=250, relief=tk.SUNKEN, borderwidth=4, bg="gray80")
center_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
details_lbl = tk.Label(master=center_frm)
details_lbl.pack(side=tk.BOTTOM, fill=tk.X)
verdict_lbl = tk.Label(master=center_frm)
verdict_lbl.pack(side=tk.BOTTOM, fill=tk.X)
move_lbl = tk.Label(master=center_frm, font=font_label)
move_lbl.pack(side=tk.TOP, fill=tk.X)
puzzle_frm = tk.Frame(master=center_frm, height=250, width=250, bg="yellow")
puzzle_frm.pack()

# Table frame contains kurang(i) table
table_frm = tk.Frame(master=window, bg="gray80")
table_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
solveable_lbl = tk.Label(master=table_frm, font=font_label)
solveable_lbl.pack(side=tk.TOP, fill=tk.X)
kurang_frm = tk.Frame(master=table_frm, bg="gray80")
kurang_frm.pack()

window.mainloop()