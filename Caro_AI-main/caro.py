import random
import pygame


class Caro:
    '''Tic Tac Toe game simulator'''

    def __init__(self, rows: int, cols: int, winning_condition: int = 5, XO: str = "X") -> None:
        '''
        Khởi tạo trò chơi với số hàng, số cột, điều kiện thắng, và người chơi bắt đầu.

        Parameters
        ------------
        rows (int): Số hàng của bảng chơi.
        cols (int): Số cột của bảng chơi.
        winning_condition (int): Số ô liên tiếp cần có để thắng trò chơi. Mặc định là 5.
        XO (str): Ký hiệu của người chơi đầu tiên (X hoặc O).
        '''
        self.originXO = XO
        self.rows = rows
        self.cols = cols
        self.grid = [['.' for _ in range(cols)] for _ in range(rows)]  # Tạo bảng chơi rỗng
        self.winning_condition = winning_condition  # Điều kiện thắng
        self.XO = XO  # Người chơi hiện tại
        self.last_move = []  # Danh sách các nước đi
        self.hard_ai = 2  # Độ khó của AI (1: dễ, 2: trung bình, 3: khó)
        self.turn = 1  # Lượt chơi hiện tại
        self.ai_turn = 2  # Lượt của AI
        self.is_use_ai = False  # Cờ kiểm tra AI có được sử dụng hay không

    def reset(self):
        '''
        Đặt lại bảng chơi về trạng thái ban đầu.
        '''
        self.grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        self.last_move = []
        self.turn = 1
        self.XO = self.originXO

    def get_possible_moves(self) -> list[list[int]]:
        '''
        Lấy tất cả các nước đi hợp lệ (các ô trống) hiện có trên bảng chơi.
        '''
        possible_moves = []
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] == '.':  # Kiểm tra ô trống
                    possible_moves.append([x, y])
        return possible_moves

    def get_all_rows(self) -> list[list[str]]:
        '''
        Trả về tất cả các hàng hiện có trên bảng chơi.
        '''
        return self.grid

    def get_all_colummns(self) -> list[list[str]]:
        '''
        Trả về tất cả các cột hiện có trên bảng chơi.
        '''
        columns = []
        for y in range(self.cols):
            col = []
            for x in range(self.rows):
                col.append(self.grid[x][y])  # Thêm các giá trị của cột
            columns.append(col)
        return columns

    def get_all_diagonals(self) -> list[list[str]]:
        '''
        Trả về tất cả các đường chéo hiện có trên bảng chơi.
        '''
        diagonals = []

        # Lấy các đường chéo từ trên trái xuống dưới phải
        for y in range(self.cols):
            diagonal = []
            x = 0
            while x < self.rows and y < self.cols:
                diagonal.append(self.grid[x][y])
                x += 1
                y += 1
            diagonals.append(diagonal)

        for x in range(1, self.rows):
            diagonal = []
            y = 0
            while x < self.rows and y < self.cols:
                diagonal.append(self.grid[x][y])
                x += 1
                y += 1
            diagonals.append(diagonal)

        # Lấy các đường chéo từ trên phải xuống dưới trái
        for y in range(self.cols):
            diagonal = []
            x = self.rows - 1
            while x >= 0 and y < self.cols:
                diagonal.append(self.grid[x][y])
                x -= 1
                y += 1
            diagonals.append(diagonal)

        for x in range(0, self.rows - 1):
            diagonal = []
            y = 0
            while x >= 0 and y < self.cols:
                diagonal.append(self.grid[x][y])
                x -= 1
                y += 1
            diagonals.append(diagonal)

        return diagonals

    def is_terminate(self) -> bool:
        '''
        Kiểm tra nếu trò chơi đã kết thúc (tất cả các ô đã được đi).
        '''
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] == '.':  # Nếu còn ô trống, trò chơi chưa kết thúc
                    return False
        return True

    def get_winner(self) -> int:
        '''
        Xác định người chiến thắng hiện tại trên bảng chơi:
        - 0 nếu người chơi với ký hiệu 'X' thắng.
        - 1 nếu người chơi với ký hiệu 'O' thắng.
        - -1 nếu không có người chơi nào thắng.
        - 2 nếu hòa.
        '''

        def check_consecutive(cons: list[list[str]]) -> int:
            for con in cons:
                count_x = 0
                count_y = 0
                for c in con:
                    if c == 'X':
                        count_x += 1
                        count_y = 0
                    elif c == 'O':
                        count_y += 1
                        count_x = 0
                    else:
                        count_x = 0
                        count_y = 0

                    if count_x == self.winning_condition:
                        return 0  # Người chơi 'X' thắng

                    if count_y == self.winning_condition:
                        return 1  # Người chơi 'O' thắng
            return -1  # Không ai thắng

        rows = self.get_all_rows()
        cols = self.get_all_colummns()
        diagonals = self.get_all_diagonals()

        winner = check_consecutive(rows)
        if winner != -1:
            return winner

        winner = check_consecutive(cols)
        if winner != -1:
            return winner

        winner = check_consecutive(diagonals)
        if winner != -1:
            return winner

        if self.is_terminate():
            return 2  # Hòa nếu không ai thắng và bảng đã đầy

        return -1  # Chưa có ai thắng hoặc hòa

    def make_move(self, x: int, y: int) -> None:
        '''
        Thực hiện một nước đi trên bảng chơi. Ký hiệu của người chơi sẽ tự động thay đổi sau lượt này.

        Parameters
        -----------
        x (int): Tọa độ x của nước đi.
        y (int): Tọa độ y của nước đi.
        '''
        if self.grid[x][y] != '.':
            return  # Không thể đi vào ô đã được đi

        self.grid[x][y] = self.XO  # Đánh dấu nước đi trên bảng
        move = (x, y)
        self.last_move.append(move)

        # Chuyển lượt cho người chơi tiếp theo
        if self.XO == 'X':
            self.XO = 'O'
        else:
            self.XO = 'X'

        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

    def change_hard_ai(self, hard: str):
        '''
        Thay đổi độ khó của AI dựa trên tham số đầu vào.
        '''
        if hard == 'easy':
            self.hard_ai = 1
        elif hard == 'hard':
            self.hard_ai = 3
        elif hard == 'medium':
            self.hard_ai = 2
        else:
            self.hard_ai = 2  # Đặt mặc định là trung bình nếu đầu vào không hợp lệ

    def use_ai(self, is_true: bool):
        '''
        Bật hoặc tắt chế độ chơi với AI.
        '''
        self.is_use_ai = is_true

    def set_ai_turn(self, turn: int):
        '''
        Đặt lượt đi của AI.
        '''
        self.ai_turn = turn

    def random_ai(self):
        '''
        Thực hiện nước đi ngẫu nhiên của AI.
        '''
        if self.ai_turn == self.turn:
            posible_move = self.get_possible_moves()
            move = random.choice(posible_move)  # Chọn nước đi ngẫu nhiên
            self.make_move(move[0], move[1])
            return True
        return False

    def get_current_XO_for_AI(self) -> str:
        '''
        Trả về ký hiệu của người chơi hiện tại mà AI đang sử dụng.
        '''
        if self.originXO == "X":
            if self.ai_turn == 2:
                return 'O'
            else:
                return 'X'
        else:
            if self.ai_turn == 1:
                return 'O'
            else:
                return 'X'


# Test
if __name__ == '__main__':
    game = Caro(15, 15)
