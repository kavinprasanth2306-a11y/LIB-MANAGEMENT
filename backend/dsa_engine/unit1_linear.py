"""
Learning Unit I: Linear Data Structures
- Stack ADT (push, pop, peek, is_empty, size)
- Expression Evaluation (Infix to Postfix & Evaluate for custom late-fee calculation)
- Queue ADT
- Circular Queue (Fixed-size buffer for Return Drop-Box)
- Deque (DoubleEndedQueue for VIP & Faculty Scheduling)
- Priority Queue (Urgency / Academic Year based reservation handling)
All implemented with raw arrays/pointers without using collections.deque or built-in dicts.
"""

class Stack:
    """Array-based Stack ADT with fixed or dynamic storage."""
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self._data = [None] * capacity
        self._top = -1

    def push(self, item):
        if self._top + 1 >= self.capacity:
            # Resize manually without list helpers
            new_cap = self.capacity * 2
            new_data = [None] * new_cap
            for i in range(self._top + 1):
                new_data[i] = self._data[i]
            self._data = new_data
            self.capacity = new_cap
        self._top += 1
        self._data[self._top] = item

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        item = self._data[self._top]
        self._data[self._top] = None
        self._top -= 1
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self._data[self._top]

    def is_empty(self) -> bool:
        return self._top == -1

    def size(self) -> int:
        return self._top + 1

    def to_list(self):
        result = []
        for i in range(self._top, -1, -1):
            result.append(self._data[i])
        return result


class Queue:
    """Basic Queue ADT implemented using dynamic array and pointers."""
    def __init__(self, capacity: int = 50):
        self.capacity = capacity
        self._data = [None] * capacity
        self._front = 0
        self._rear = 0
        self._count = 0

    def enqueue(self, item):
        if self._count == self.capacity:
            new_cap = self.capacity * 2
            new_data = [None] * new_cap
            for i in range(self._count):
                new_data[i] = self._data[(self._front + i) % self.capacity]
            self._data = new_data
            self._front = 0
            self._rear = self._count
            self.capacity = new_cap

        self._data[self._rear] = item
        self._rear = (self._rear + 1) % self.capacity
        self._count += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self.capacity
        self._count -= 1
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self._data[self._front]

    def is_empty(self) -> bool:
        return self._count == 0

    def size(self) -> int:
        return self._count

    def to_list(self):
        result = []
        for i in range(self._count):
            result.append(self._data[(self._front + i) % self.capacity])
        return result


class CircularQueue:
    """
    Fixed-size Circular Queue for Return Drop-Box Buffering.
    Demonstrates modulo arithmetic and fixed-buffer wrap-around.
    """
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self._data = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    def is_full(self) -> bool:
        return (self.rear + 1) % self.capacity == self.front

    def is_empty(self) -> bool:
        return self.front == -1

    def enqueue(self, item) -> bool:
        if self.is_full():
            return False  # Drop-box buffer is full
        if self.is_empty():
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity
        self._data[self.rear] = item
        self.count += 1
        return True

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty circular queue")
        item = self._data[self.front]
        self._data[self.front] = None
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        self.count -= 1
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self._data[self.front]

    def get_state(self):
        """Returns internal buffer slots and pointer indices for visualization."""
        slots = []
        for i in range(self.capacity):
            slots.append({
                "index": i,
                "value": self._data[i],
                "is_front": (i == self.front),
                "is_rear": (i == self.rear)
            })
        return {
            "capacity": self.capacity,
            "front": self.front,
            "rear": self.rear,
            "count": self.count,
            "is_full": self.is_full(),
            "is_empty": self.is_empty(),
            "slots": slots
        }

    def to_list(self):
        if self.is_empty():
            return []
        res = []
        idx = self.front
        while True:
            res.append(self._data[idx])
            if idx == self.rear:
                break
            idx = (idx + 1) % self.capacity
        return res


class DoubleEndedQueue:
    """
    Double-Ended Queue (Deque) for VIP & Faculty Scheduling.
    Faculty/VIP items are inserted at front; standard requests at rear.
    """
    def __init__(self, capacity: int = 30):
        self.capacity = capacity
        self._data = [None] * capacity
        self.front = -1
        self.rear = 0
        self.count = 0

    def is_full(self) -> bool:
        return ((self.front == 0 and self.rear == self.capacity - 1) or
                (self.front == self.rear + 1))

    def is_empty(self) -> bool:
        return self.front == -1

    def insert_front(self, item):
        if self.is_full():
            # expand capacity
            self._resize()

        if self.front == -1:
            self.front = 0
            self.rear = 0
        elif self.front == 0:
            self.front = self.capacity - 1
        else:
            self.front = self.front - 1

        self._data[self.front] = item
        self.count += 1

    def insert_rear(self, item):
        if self.is_full():
            self._resize()

        if self.front == -1:
            self.front = 0
            self.rear = 0
        elif self.rear == self.capacity - 1:
            self.rear = 0
        else:
            self.rear = self.rear + 1

        self._data[self.rear] = item
        self.count += 1

    def delete_front(self):
        if self.is_empty():
            raise IndexError("delete_front from empty deque")
        item = self._data[self.front]
        self._data[self.front] = None
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            if self.front == self.capacity - 1:
                self.front = 0
            else:
                self.front = self.front + 1
        self.count -= 1
        return item

    def delete_rear(self):
        if self.is_empty():
            raise IndexError("delete_rear from empty deque")
        item = self._data[self.rear]
        self._data[self.rear] = None
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        elif self.rear == 0:
            self.rear = self.capacity - 1
        else:
            self.rear = self.rear - 1
        self.count -= 1
        return item

    def get_front(self):
        if self.is_empty():
            return None
        return self._data[self.front]

    def get_rear(self):
        if self.is_empty():
            return None
        return self._data[self.rear]

    def _resize(self):
        new_cap = self.capacity * 2
        new_data = [None] * new_cap
        for i in range(self.count):
            new_data[i] = self._data[(self.front + i) % self.capacity]
        self._data = new_data
        self.front = 0
        self.rear = self.count - 1
        self.capacity = new_cap

    def to_list(self):
        if self.is_empty():
            return []
        items = []
        for i in range(self.count):
            items.append(self._data[(self.front + i) % self.capacity])
        return items

    def get_state(self):
        return {
            "capacity": self.capacity,
            "front": self.front,
            "rear": self.rear,
            "count": self.count,
            "items": self.to_list()
        }


class PriorityQueue:
    """
    Priority Queue for academic year / urgency reservation handling.
    Lower number or higher priority depending on config.
    Here: higher priority score = served first.
    Item format: (priority, data)
    Implemented via ordered insertion or custom heap.
    """
    def __init__(self, capacity: int = 50):
        self.capacity = capacity
        self._data = [None] * capacity
        self.count = 0

    def enqueue(self, item, priority: int):
        if self.count == self.capacity:
            new_cap = self.capacity * 2
            new_data = [None] * new_cap
            for i in range(self.count):
                new_data[i] = self._data[i]
            self._data = new_data
            self.capacity = new_cap

        # Find position based on priority (Descending order: highest priority at front)
        idx = self.count - 1
        while idx >= 0 and self._data[idx]["priority"] < priority:
            self._data[idx + 1] = self._data[idx]
            idx -= 1

        self._data[idx + 1] = {"priority": priority, "data": item}
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty PriorityQueue")
        item = self._data[0]
        # Shift elements left
        for i in range(1, self.count):
            self._data[i - 1] = self._data[i]
        self._data[self.count - 1] = None
        self.count -= 1
        return item

    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self) -> bool:
        return self.count == 0

    def size(self) -> int:
        return self.count

    def to_list(self):
        res = []
        for i in range(self.count):
            res.append(self._data[i])
        return res


def evaluate_infix_expression(expression: str, variables=None) -> dict:
    """
    Custom Expression Evaluator for late-fee calculation:
    Converts Infix -> Postfix using Stack, then evaluates Postfix.
    Supports variables like {days: 5, rate: 2, fee: 10}.
    Returns evaluation result and detailed step trace for UI.
    """
    if variables is None:
        variables = {}

    def get_var_value(name):
        for k, v in variables.items():
            if k == name:
                return v
        return 0

    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        c = expression[i]
        if c == ' ':
            i += 1
            continue
        if c in '+-*/()^':
            tokens.append(c)
            i += 1
        elif c.isdigit() or c == '.':
            num_str = ""
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            tokens.append(float(num_str))
        elif c.isalpha() or c == '_':
            var_str = ""
            while i < n and (expression[i].isalnum() or expression[i] == '_'):
                var_str += expression[i]
                i += 1
            # Replace variable with value
            val = get_var_value(var_str)
            tokens.append(float(val))
        else:
            i += 1

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = Stack(50)
    postfix = []
    conversion_steps = []

    for token in tokens:
        if isinstance(token, float):
            postfix.append(token)
            conversion_steps.append({"token": token, "action": f"Output operand {token}", "stack": stack.to_list()})
        elif token == '(':
            stack.push(token)
            conversion_steps.append({"token": token, "action": "Push ( to stack", "stack": stack.to_list()})
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                postfix.append(stack.pop())
            if not stack.is_empty() and stack.peek() == '(':
                stack.pop()  # Discard '('
            conversion_steps.append({"token": token, "action": "Popped till (", "stack": stack.to_list()})
        else:
            # Operator
            token_prec = precedence.get(token, 0)
            while not stack.is_empty() and stack.peek() != '(' and precedence.get(stack.peek(), 0) >= token_prec:
                postfix.append(stack.pop())
            stack.push(token)
            conversion_steps.append({"token": token, "action": f"Push operator {token}", "stack": stack.to_list()})

    while not stack.is_empty():
        postfix.append(stack.pop())

    # Evaluation of postfix
    eval_stack = Stack(50)
    eval_steps = []
    for token in postfix:
        if isinstance(token, float):
            eval_stack.push(token)
            eval_steps.append({"token": token, "action": f"Push number {token}", "stack": eval_stack.to_list()})
        else:
            if eval_stack.size() < 2:
                raise ValueError("Malformed expression")
            b = eval_stack.pop()
            a = eval_stack.pop()
            res = 0.0
            if token == '+':
                res = a + b
            elif token == '-':
                res = a - b
            elif token == '*':
                res = a * b
            elif token == '/':
                res = a / b if b != 0 else 0.0
            elif token == '^':
                res = a ** b
            eval_stack.push(res)
            eval_steps.append({"token": token, "action": f"Compute {a} {token} {b} = {res}", "stack": eval_stack.to_list()})

    final_result = eval_stack.pop() if not eval_stack.is_empty() else 0.0

    return {
        "expression": expression,
        "variables": variables,
        "postfix": [str(x) for x in postfix],
        "result": round(final_result, 2),
        "conversion_steps": conversion_steps,
        "eval_steps": eval_steps
    }
