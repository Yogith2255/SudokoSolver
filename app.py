from flask import Flask, render_template, jsonify, request
from sudoku_logic import SudokuSolver

app = Flask(__name__)
solver = SudokuSolver()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/hint', methods=['POST'])
def hint():
    board = request.json['board']
    hint_data = solver.get_hint(board)
    
    if hint_data:
        return jsonify({"status": "success", "hint": hint_data})
    else:
        return jsonify({"status": "error", "message": "No hint available"}), 400

@app.route('/generate', methods=['GET'])
def generate():
    # Get level from query parameters, default to Medium
    level = request.args.get('level', 'Medium')
    board = solver.generate_puzzle(level)
    return jsonify({"board": board})

@app.route('/solve', methods=['POST'])
def solve():
    board = request.json['board']
    
    # Check if the board is valid before solving
    is_valid, error_pos = solver.is_board_valid(board)
    if not is_valid:
        return jsonify({
            "status": "error", 
            "message": f"Invalid input at Row {error_pos[0]+1}, Col {error_pos[1]+1}",
            "error_pos": error_pos
        }), 400

    solver.solve(board)
    return jsonify({"status": "success", "solution": board})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
