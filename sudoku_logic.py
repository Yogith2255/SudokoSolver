import random

class SudokuSolver:
    def is_valid(self, board, r, c, k):
        for i in range(9):
            if board[i][c] == k: return False
            if board[r][i] == k: return False
            if board[3*(r//3) + i//3][3*(c//3) + i%3] == k: return False
        return True
    def is_board_valid(self, board):
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == ".":
                    continue
                board[r][c] = "."
                if not self.is_valid(board, r, c, val):
                    board[r][c] = val 
                    return False, (r, c) 
                board[r][c] = val
        return True, None

    def solve(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    for k in "123456789":
                        if self.is_valid(board, i, j, k):
                            board[i][j] = k
                            if self.solve(board): return True
                            board[i][j] = "."
                    return False
        return True
    def get_hint(self, current_board):
        # 1. Create a copy and solve it to find the correct values
        solution = [row[:] for row in current_board]
        if not self.solve(solution):
            return None # Board is unsolvable
            
        # 2. Find all empty cells
        empty_cells = []
        for r in range(9):
            for c in range(9):
                if current_board[r][c] == ".":
                    empty_cells.append((r, c))
        
        if not empty_cells:
            return None # Board is already full
            
        # 3. Pick one random empty cell and return its solution
        r, c = random.choice(empty_cells)
        return {"row": r, "col": c, "value": solution[r][c]}

    def generate_puzzle(self, level="Medium"):
        # Map difficulty levels to number of empty cells to create
        # Easy: ~35-40 clues left (45 removed)
        # Medium: ~30 clues left (51 removed)
        # Hard: ~20-25 clues left (58 removed)
        difficulty_map = {
            "Easy": 40,
            "Medium": 50,
            "Hard": 60
        }
        remove_count = difficulty_map.get(level, 50)

        board = [["." for _ in range(9)] for _ in range(9)]
        
        for i in range(0, 9, 3):
            nums = list("123456789")
            random.shuffle(nums)
            for r in range(3):
                for c in range(3):
                    board[i+r][i+c] = nums.pop()
        
        self.solve(board) 
        
       
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        for i in range(remove_count):
            r, c = cells[i]
            board[r][c] = "."
            
        return board