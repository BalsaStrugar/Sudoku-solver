import tkinter as tk
from tkinter import messagebox

class Board:
    def __init__(self, board):
        self.board = board

    def __str__(self):
        board_str = ''
        for row in self.board:
            row_str = [str(i) if i else '*' for i in row]
            board_str += ' '.join(row_str)
            board_str += '\n'
        return board_str

    def find_empty_cell(self):
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0)
                return row, col
            except ValueError:
                pass
        return None

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return all(self.board[row][col] != num for row in range(9))

    def valid_in_square(self, row, col, num):
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3):
                if self.board[row_no][col_no] == num:
                    return False
        return True

    def is_valid(self, empty, num):
        row, col = empty
        valid_in_row = self.valid_in_row(row, num)
        valid_in_col = self.valid_in_col(col, num)
        valid_in_square = self.valid_in_square(row, col, num)
        return all([valid_in_row, valid_in_col, valid_in_square])

    def solver(self):
        if (next_empty := self.find_empty_cell()) is None:
            return True
        for guess in range(1, 10):
            if self.is_valid(next_empty, guess):
                row, col = next_empty
                self.board[row][col] = guess
                if self.solver():
                    return True
                self.board[row][col] = 0
        return False

def solve_sudoku(board):
    gameboard = Board(board)
    return gameboard.solver(), gameboard.board

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku solver")
        
        self.entries = [[tk.Entry(root, width=3, font=('Arial', 18), justify='center') 
                         for _ in range(9)] for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                self.entries[i][j].grid(row=i, column=j, padx=2, pady=2)
        
        self.solve_button = tk.Button(root, text="Reši", font=('Arial', 18), command=self.solve)
        self.solve_button.grid(row=9, column=0, columnspan=9, pady=20)

        self.reset_button = tk.Button(root, text="Resetuj", font=('Arial', 18), command=self.reset)
        self.reset_button.grid(row=10, column=0, columnspan=9, pady=20)

    def get_board_from_input(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == '':
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            row.append(0)
                    except ValueError:
                        row.append(0)
            board.append(row)
        return board

    def solve(self):
        board = self.get_board_from_input()
        solvable, solved_board = solve_sudoku(board)
        
        if solvable:
            self.update_grid(solved_board)
        else:
            messagebox.showerror("Greška", "Ne postoji rešenje za ovu sudoku tablu.")

    def update_grid(self, solved_board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(solved_board[i][j]))

    def reset(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)

def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
