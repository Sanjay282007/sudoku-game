:- use_module(library(clpfd)).

% -------------------- [CSP + FOL + BACKTRACKING BEGIN] --------------------
% Main Sudoku Solver Rule
sudoku(Puzzle, Solution) :-
    maplist(replace_zeros, Puzzle, PuzzleVars),
    Solution = PuzzleVars,
    append(Solution, Vars), Vars ins 1..9,     % CSP: Domain [1..9]

    maplist(all_distinct, Solution),           % FOL: Rows must be unique
    transpose(Solution, Columns),
    maplist(all_distinct, Columns),            % FOL: Columns must be unique
    blocks(Solution),                          % FOL: 3x3 blocks must be unique

    maplist(label, Solution).                  % BACKTRACKING + CSP: Tries values recursively
    
% -------------------- [CSP + FOL + BACKTRACKING END] --------------------

% Replace 0s with fresh Prolog variables
replace_zeros([], []).
replace_zeros([0|T1], [_|T2]) :- replace_zeros(T1, T2).
replace_zeros([H|T1], [H|T2]) :- H \= 0, replace_zeros(T1, T2).

% Block checking
blocks([]).
blocks([A,B,C|Rest]) :-
    block3(A, B, C),
    blocks(Rest).

block3([], [], []).
block3([A,B,C|R1], [D,E,F|R2], [G,H,I|R3]) :-
    all_distinct([A,B,C,D,E,F,G,H,I]),
    block3(R1, R2, R3).

% Entry point for solving
solve(Puzzle) :-
    sudoku(Puzzle, Solution),
    print_solution(Solution).

% Display the solution
print_solution([]).
print_solution([Row|Rest]) :-
    format('~w~n', [Row]),
    print_solution(Rest).
