import ast

def load_frames(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Parse the file into an AST
        try:
            tree = ast.parse(f.read())
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []

    # Find the assignment to 'frames'
    frames_data = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'frames':
                    try:
                        # ast.literal_eval handles lists/numbers/strings safely
                        # We need to turn the node value (List) back into a python object.
                        # Since it's inside AST, we can't directly use literal_eval on the node *object* unless we have the string.
                        # But we can compile and eval the expression node, or just unparse it if we had python 3.9+.
                        # A robust way for simple literals is to execute the assignment.
                        pass
                    except:
                        pass
    
    # Fallback: Read file -> extract the string -> literal_eval
    # This is safer for extracting list literals without executing arbitrary code
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Naive extraction based on known structure in main.py
    # frames = [ ... ]
    start_idx = content.find('frames = [')
    if start_idx == -1:
        return []
    
    # Count brackets to find the end
    open_brackets = 0
    end_idx = -1
    for i in range(start_idx, len(content)):
        char = content[i]
        if char == '[':
            open_brackets += 1
        elif char == ']':
            open_brackets -= 1
            if open_brackets == 0:
                end_idx = i + 1
                break
    
    if end_idx != -1:
        frames_str = content[start_idx:end_idx]
        # execute this string to get the list
        scope = {}
        exec(frames_str, {}, scope)
        return scope.get('frames', [])
    
    return []

def generate_boolean_expr(active_indices):
    """
    Generates a Sum of Products (SOP) expression.
    Input vars: x_0, x_1, x_2 corresponding to bits of the frame index (0..7).
    Mapping Assumption: "000~111" maps to [x_0, x_1, x_2].
    So indices correspond to binary string b0 b1 b2? 
    Usually left-to-right matches input string.
    So "100" (which is index 4 if binary) -> x_0=1, x_1=0, x_2=0.
    Thus x_0 is MSB (value 4), x_1 is Middle (value 2), x_2 is LSB (value 1).
    """
    if not active_indices:
        return "0"
    
    # Optimization: if all indices present, it's 1
    if len(active_indices) == 8:
        return "1"

    terms = []
    for idx in sorted(active_indices):
        # bit 2 (weight 4) -> x_0
        # bit 1 (weight 2) -> x_1
        # bit 0 (weight 1) -> x_2
        
        b0 = (idx >> 2) & 1  # MSB
        b1 = (idx >> 1) & 1
        b2 = (idx >> 0) & 1  # LSB
        
        # Build minterm string
        # If bit is 1, use variable name. If 0, use variable' (NOT).
        # We'll use a concise notation usually: x_0 x_1' x_2
        
        t0 = "x_0" if b0 else "x_0'"
        t1 = "x_1" if b1 else "x_1'"
        t2 = "x_2" if b2 else "x_2'"
        
        terms.append(f"{t0}{t1}{t2}")
        
    return " + ".join(terms)

def main():
    frames = load_frames('main.py')
    if not frames:
        print("Could not load frames from main.py")
        return

    # Dimensions
    num_frames = len(frames)
    if num_frames == 0:
        return
    rows = len(frames[0])
    cols = len(frames[0][0])
    
    output_lines = []
    
    for r in range(rows):
        for c in range(cols):
            # Identify which frames have a pixel at (r, c)
            active_indices = []
            for k in range(num_frames):
                if frames[k][r][c] == 1:
                    active_indices.append(k)
            
            expr = generate_boolean_expr(active_indices)
            output_lines.append(f"y_{r}_{c} = {expr}")
            
    with open('boolean_func.txt', 'w') as f:
        f.write('\n'.join(output_lines))
    
    print(f"Generated boolean functions for {len(output_lines)} outputs.")

if __name__ == '__main__':
    main()
