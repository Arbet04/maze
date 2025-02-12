import turtle
import time

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'

class Maze:
    def __init__(self, maze_file_name):
        self.maze_list = []
        maze_file = open(maze_file_name, 'r')
        self.rows_in_maze = 0

        for line in maze_file:
            row_list = []
            col = 0
            for ch in line.strip():
                row_list.append(ch)
                if ch == 'S':
                    self.start_row = self.rows_in_maze
                    self.start_col = col
                col += 1
            self.rows_in_maze += 1
            self.maze_list.append(row_list)
        
        self.columns_in_maze = len(self.maze_list[0])
        self.x_translate = -self.columns_in_maze / 2
        self.y_translate = self.rows_in_maze / 2

        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(
            -(self.columns_in_maze - 1) / 2 - 0.5,
            -(self.rows_in_maze - 1) / 2 - 0.5,
            (self.columns_in_maze - 1) / 2 + 0.5,
            (self.rows_in_maze - 1) / 2 + 0.5
        )
        self.draw_maze()

    def draw_maze(self):
        self.t.speed(10)
        for y in range(self.rows_in_maze):
            for x in range(self.columns_in_maze):
                if self.maze_list[y][x] == OBSTACLE:
                    self.draw_centered_box(x + self.x_translate, -y + self.y_translate, 'orange')
        self.t.color('black')
        self.t.fillcolor('blue')

    def draw_centered_box(self, x, y, color):
        self.t.up()
        self.t.goto(x - 0.5, y - 0.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for _ in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def move_turtle(self, x, y):
        self.t.up()
        self.t.setheading(self.t.towards(x + self.x_translate, -y + self.y_translate))
        self.t.goto(x + self.x_translate, -y + self.y_translate)

    def drop_bread_crumb(self, color):
        self.t.dot(10, color)

    def update_position(self, row, col, val=None):
        if val:
            self.maze_list[row][col] = val
        self.move_turtle(col, row)
        color_map = {PART_OF_PATH: 'green', OBSTACLE: 'red', TRIED: 'black', DEAD_END: 'red'}
        if val in color_map:
            self.drop_bread_crumb(color_map[val])

    def is_exit(self, row, col):
        return row == 0 or row == self.rows_in_maze - 1 or col == 0 or col == self.columns_in_maze - 1

    def __getitem__(self, idx):
        return self.maze_list[idx]


def search_from(maze, start_row, start_column):
    if maze[start_row][start_column] == OBSTACLE:
        return False
    if maze.is_exit(start_row, start_column):
        maze.update_position(start_row, start_column, PART_OF_PATH)
        return True
    if maze[start_row][start_column] in [TRIED, DEAD_END]:
        return False

    maze.update_position(start_row, start_column, TRIED)
    time.sleep(0.2)

    for d_row, d_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = start_row + d_row, start_column + d_col
        if search_from(maze, new_row, new_col):
            maze.update_position(start_row, start_column, PART_OF_PATH)
            return True

    maze.update_position(start_row, start_column, DEAD_END)
    return False


if __name__ == "__main__":
    maze = Maze("maze2.txt")
    search_from(maze, maze.start_row, maze.start_col)
    maze.wn.mainloop()