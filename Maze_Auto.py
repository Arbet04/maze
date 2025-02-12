import os
import time
from Stack import Stack

class maze:
    def __init__(self) -> None:
        self.maze = [
                    ["X", "X", "X", "X", "X", "X", "X"],
                    ["X", " ", " ", " ", "X", " ", "X"],
                    ["X", " ", "X", " ", "X", " ", " "],
                    ["X", " ", "X", " ", "X", " ", "X"],
                    ["X", " ", "X", " ", " ", " ", "X"],
                    ["X", " ", "X", "X", "X", "X", "X"],
                    ]
        self.ply = pos(5, 1)
        self.end = pos(2, 6)
        self.maze[self.ply.y][self.ply.x] = "P"
        self.maze[self.end.y][self.end.x] = "E"
        self.directions = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}

    def isInBound(self, y, x):
        return 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0])

    def print(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n\n\n")
        for row in self.maze:
            print(" ".join(row))
        print("\n\n\n")

    def printEND(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("\n\n\n")
        print(">>>>> Congratulations!!! <<<<<")
        print("\n\n\n")

    def Visited(self):
        stack = Stack()
        stack.push((self.ply.y, self.ply.x))  
        visited = set()  
        path = []  # เก็บเส้นทางที่เดินผ่านมา

        while not stack.isEmpty():
            current_y, current_x = stack.pop()
            self.ply.y, self.ply.x = current_y, current_x  
            self.maze[current_y][current_x] = "P"  # วาง "P" ที่ตำแหน่งปัจจุบัน
            self.print()
            time.sleep(0.25)

            if (current_y, current_x) == (self.end.y, self.end.x):
                self.printEND()
                return True

            visited.add((current_y, current_x))
            possible_moves = []

            for direction in [1, 2, 3, 4]:  # ตรวจสอบ 4 ทิศทาง
                dy, dx = self.directions[direction]
                next_y, next_x = current_y + dy, current_x + dx

                if self.isInBound(next_y, next_x) and (next_y, next_x) not in visited:
                    if self.maze[next_y][next_x] in [" ", "E"]:
                        possible_moves.append((next_y, next_x))

            if possible_moves:
                for move in possible_moves:
                    stack.push(move)
                # เปลี่ยนตำแหน่งก่อนหน้าของ "P" ให้เป็น "."
                if path:
                    prev_y, prev_x = path[-1]
                    self.maze[prev_y][prev_x] = "."
                path.append((current_y, current_x))
            else:
                # ไม่มีทางไป → ลบ "." ทั้งหมดที่เป็น Dead-end และย้อนกลับ
                while path:
                    back_y, back_x = path.pop()
                    self.maze[back_y][back_x] = " "  # เปลี่ยนกลับเป็น " "
                    self.print()
                    time.sleep(0.1)
                    if any(
                        self.isInBound(back_y + dy, back_x + dx) and
                        self.maze[back_y + dy][back_x + dx] in [" ", "E"]
                        for dy, dx in self.directions.values()
                    ):
                        break  # หยุดย้อนกลับถ้าพบทางใหม่

        print("No path to the exit.")
        return False


class pos:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x


if __name__ == '__main__':
    m = maze()
    m.print()
    m.Visited()  # เรียกใช้ฟังก์ชันเพื่อให้ "P" เดินออกจากเขาวงกต
