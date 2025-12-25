import csv
import sys
import os

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

try:
    from construct_boolean_func import load_frames, generate_boolean_expr
except ImportError:
    # If import fails (e.g. running from a different dir), try to copy/paste the load_frames logic or warn
    # For now, we assume the environment allows importing from adjacent files in the same workspace.
    print("Error: Could not import load_frames from construct_boolean_func.py")
    sys.exit(1)

def main():
    input_file = 'main.py'
    frames = load_frames(input_file)
    
    if not frames:
        print(f"No frames loaded from {input_file}")
        return

    num_frames = len(frames)
    if num_frames == 0:
        return

    rows = len(frames[0])
    cols = len(frames[0][0])
    
    output_filename = 'truth_table.csv'
    
    print(f"Generating truth table for {num_frames} states (rows={rows}, cols={cols})...")
    
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # 1. Write Header
        # Inputs: x_0 (MSB), x_1, x_2 (LSB) based on 3-bit logic in construct_boolean_func.py
        header = ['x_0', 'x_1', 'x_2']
        
        # Outputs: y_r_c
        outputs = []
        for r in range(rows):
            for c in range(cols):
                outputs.append(f"y_{r}_{c}")
        
        writer.writerow(header + outputs)
        
        # 2. Write Rows
        for i in range(num_frames):
            # Determine input bits for index i
            # Matches logic in construct_boolean_func.generate_boolean_expr
            # b0 = (idx >> 2) & 1  # MSB
            # b1 = (idx >> 1) & 1
            # b2 = (idx >> 0) & 1  # LSB
            
            x0 = (i >> 2) & 1
            x1 = (i >> 1) & 1
            x2 = (i >> 0) & 1
            
            row_inputs = [x0, x1, x2]
            
            row_outputs = []
            for r in range(rows):
                for c in range(cols):
                    val = frames[i][r][c]
                    row_outputs.append(val)
            
            writer.writerow(row_inputs + row_outputs)
            
    print(f"Successfully wrote truth table to {output_filename}")

if __name__ == "__main__":
    main()
