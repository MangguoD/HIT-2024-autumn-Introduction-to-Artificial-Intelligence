__author__ = 'MangguoD'

class State:
    def __init__(self, monkey_pos, box_pos, banana_pos, room_layout, path=None):
        self.monkey_pos = monkey_pos
        self.box_pos = box_pos
        self.banana_pos = banana_pos
        self.room_layout = room_layout  # 房间布局
        self.path = path if path is not None else []

    def is_goal(self):
        # 只有当猴子在箱子上并且猴子和香蕉的坐标重合时，才能摘到香蕉
        return self.monkey_pos == self.banana_pos and self.monkey_pos == self.box_pos

    def is_within_bounds(self, position):
        x, y = position
        # 检查位置是否在房间内且是可通行的
        return (0 <= x < len(self.room_layout) and
                0 <= y < len(self.room_layout[0]) and
                self.room_layout[x][y] == 0)

def get_possible_moves(state):
    moves = []
    # 假设猴子可以在房间内移动
    for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # 右、左、上、下
        new_monkey_pos = (state.monkey_pos[0] + move[0], state.monkey_pos[1] + move[1])
        if state.is_within_bounds(new_monkey_pos):  # 检查是否在房间内
            moves.append(State(new_monkey_pos, state.box_pos, state.banana_pos, state.room_layout, state.path + [new_monkey_pos]))

    # 如果猴子在箱子旁边，可以移动箱子
    if state.monkey_pos == state.box_pos:
        for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_box_pos = (state.box_pos[0] + move[0], state.box_pos[1] + move[1])
            if state.is_within_bounds(new_box_pos):  # 检查是否在房间内
                moves.append(State(state.monkey_pos, new_box_pos, state.banana_pos, state.room_layout, state.path + [new_box_pos]))

    return moves

def bfs(initial_state):
    from collections import deque
    queue = deque([initial_state])
    visited = set()

    while queue:
        current_state = queue.popleft()

        if current_state.is_goal():
            return current_state.path  # 返回移动路径

        visited.add((current_state.monkey_pos, current_state.box_pos))

        for next_state in get_possible_moves(current_state):
            if (next_state.monkey_pos, next_state.box_pos) not in visited:
                queue.append(next_state)

    return None

# 示例房间布局
# 0 表示可通行，1 表示不可通行
room_layout = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

# 示例初始状态
initial_state = State((0, 0), (4, 4), (0, 2), room_layout)
result = bfs(initial_state)

if result is not None:
    print("猴子能摘到香蕉，移动路径为:", result)
else:
    print("猴子无法摘到香蕉")