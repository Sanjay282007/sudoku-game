import sys
import subprocess
import ast
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

PUZZLES = [
    [
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],
        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],
        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9]
    ],
    [
        [0,2,0, 6,0,8, 0,0,0],
        [5,8,0, 0,0,9, 7,0,0],
        [0,0,0, 0,4,0, 0,0,0],
        [3,7,0, 0,0,0, 5,0,0],
        [6,0,0, 0,0,0, 0,0,4],
        [0,0,8, 0,0,0, 0,1,3],
        [0,0,0, 0,2,0, 0,0,0],
        [0,0,9, 8,0,0, 0,3,6],
        [0,0,0, 3,0,6, 0,9,0]
    ],
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 8, 0, 0, 0, 7, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 7, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 3],
        [0, 9, 0, 4, 0, 0, 0, 7, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0]
    ],
    [
        [1, 0, 0, 4, 8, 9, 0, 0, 6],
        [7, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 9, 0, 0, 0, 6, 0, 0, 0],
        [5, 0, 0, 1, 0, 2, 0, 0, 8],
        [0, 0, 0, 9, 0, 0, 0, 3, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 6, 9],
        [6, 0, 0, 5, 1, 3, 0, 0, 2]
    ]
]

class SudokuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Sudoku Solver")
        self.setFixedSize(700, 800)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        self.puzzle_index = 0
        self.cells = [[QLineEdit() for _ in range(9)] for _ in range(9)]
        self.solution = None
        self.default_cells = set()

        self.setStyleSheet("background-color: white; color: black;")
        self.init_ui()
        self.load_puzzle(PUZZLES[self.puzzle_index])

    def init_ui(self):
        title = QLabel("Sudoku with AI Solver")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: black;")

        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                cell.setFixedSize(60, 60)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFont(QFont("Arial", 16))
                cell.setStyleSheet("""
                    QLineEdit {
                        background-color: white;
                        color: black;
                        border: 1px solid black;
                    }
                """)
                cell.textChanged.connect(self.validate_cell(i, j))
                self.grid.addWidget(cell, i, j)

        btn_solve = QPushButton("Solve with AI")
        btn_hint = QPushButton("Get Hint")
        btn_submit = QPushButton("Submit")
        btn_new = QPushButton("New Game")

        for btn in [btn_solve, btn_hint, btn_submit, btn_new]:
            btn.setStyleSheet("background-color: white; color: black; border: 1px solid black;")

        btn_solve.clicked.connect(self.solve)
        btn_hint.clicked.connect(self.get_hint)
        btn_submit.clicked.connect(self.submit)
        btn_new.clicked.connect(self.new_game)

        btn_layout = QHBoxLayout()
        for btn in [btn_solve, btn_hint, btn_submit, btn_new]:
            btn_layout.addWidget(btn)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        grid_container = QWidget()
        grid_container.setLayout(self.grid)
        layout.addWidget(title)
        layout.addWidget(grid_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def validate_cell(self, i, j):
        def inner():
            if (i, j) in self.default_cells:
                return

            text = self.cells[i][j].text()
            if text == "":
                self.cells[i][j].setStyleSheet("background-color: white; color: black; border: 1px solid black;")
            else:
                try:
                    value = int(text)
                    if 1 <= value <= 9:
                        if self.solution and value != self.solution[i][j]:
                            self.cells[i][j].setStyleSheet("background-color: red; color: black; border: 1px solid black;")
                        else:
                            self.cells[i][j].setStyleSheet("background-color: white; color: black; border: 1px solid black;")
                    else:
                        self.cells[i][j].setStyleSheet("background-color: red; color: black; border: 1px solid black;")
                except ValueError:
                    self.cells[i][j].setStyleSheet("background-color: red; color: black; border: 1px solid black;")
        return inner

    def load_puzzle(self, puzzle):
        self.default_cells.clear()
        for i in range(9):
            for j in range(9):
                val = puzzle[i][j]
                cell = self.cells[i][j]
                if val != 0:
                    cell.setText(str(val))
                    cell.setReadOnly(True)
                    cell.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
                    self.default_cells.add((i, j))
                else:
                    cell.setText('')
                    cell.setReadOnly(False)
                    cell.setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        self.solution = self.run_prolog_solver(puzzle)

    def get_current_puzzle(self):
        puzzle = []
        for i in range(9):
            row = []
            for j in range(9):
                text = self.cells[i][j].text()
                try:
                    num = int(text)
                    row.append(num if 1 <= num <= 9 else 0)
                except ValueError:
                    row.append(0)
            puzzle.append(row)
        return puzzle

    def solve(self):
        if self.solution:
            self.load_puzzle(self.solution)
        else:
            QMessageBox.warning(self, "Error", "No solution found!")

    def get_hint(self):
        if self.solution:
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j].text() == '':
                        self.cells[i][j].setText(str(self.solution[i][j]))
                        return
        else:
            QMessageBox.warning(self, "Error", "No solution found!")

    def submit(self):
        if not self.solution:
            QMessageBox.warning(self, "Error", "Solution not available for validation.")
            return

        correct = True
        for i in range(9):
            for j in range(9):
                if (i, j) in self.default_cells:
                    continue
                user_val = self.cells[i][j].text()
                correct_val = str(self.solution[i][j])
                if user_val != correct_val:
                    self.cells[i][j].setStyleSheet("background-color: red; color: black; border: 1px solid black;")
                    correct = False
                else:
                    self.cells[i][j].setStyleSheet("background-color: white; color: black; border: 1px solid black;")
        if correct:
            QMessageBox.information(self, "Success", "Congratulations! You solved the puzzle!")
        else:
            QMessageBox.warning(self, "Incorrect", "Solution is not correct.")

    def new_game(self):
        self.puzzle_index = (self.puzzle_index + 1) % len(PUZZLES)
        self.load_puzzle(PUZZLES[self.puzzle_index])

    def run_prolog_solver(self, puzzle):
        prolog_query = f"solve({puzzle}), halt."
        try:
            result = subprocess.run(
                ['swipl', '-s', 'sudoku_solver.pl', '-g', prolog_query],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print("Prolog Error:\n", result.stderr)
                return None

            lines = result.stdout.strip().split('\n')
            solution = [ast.literal_eval(line) for line in lines if line.startswith('[')]
            return solution
        except Exception as e:
            print("Error running Prolog:", e)
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SudokuGUI()
    gui.show()
    sys.exit(app.exec())
