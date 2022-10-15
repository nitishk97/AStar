from cellState import cellState


def priorityComparision(state1: cellState, stateSign: str, state2: cellState, largerGFirst: bool):
    if largerGFirst is True:
        if stateSign == "==":
            return largerGPriority(state1) == largerGPriority(state2)
        elif stateSign == ">":
            return largerGPriority(state1) > largerGPriority(state2)
        elif stateSign == "<":
            return largerGPriority(state1) < largerGPriority(state2)
        elif stateSign == ">=":
            return largerGPriority(state1) >= largerGPriority(state2)
        elif stateSign == "<=":
            return largerGPriority(state1) <= largerGPriority(state2)
    else:
        if stateSign == "==":
            return smallerGPriority(state1) == smallerGPriority(state2)
        elif stateSign == ">":
            return smallerGPriority(state1) > smallerGPriority(state2)
        elif stateSign == "<":
            return smallerGPriority(state1) < smallerGPriority(state2)
        elif stateSign == ">=":
            return smallerGPriority(state1) >= smallerGPriority(state2)
        elif stateSign == "<=":
            return smallerGPriority(state1) <= smallerGPriority(state2)


def largerGPriority(state: cellState):
    return 999 * state.f_value - state.g_value


def smallerGPriority(state: cellState):
    return 999 * state.f_value + state.g_value


class MinHeap(object):
    def __init__(self, largerGFirst: bool):
        self.heap_data = []
        self.cnt = len(self.heap_data)
        self.largerGFirst = largerGFirst

    def heap_size(self):
        return self.cnt

    def isEmpty(self):
        return self.cnt == 0

    def push(self, ele):
        self.heap_data.append(ele)
        self.cnt += 1
        self.shiftUpward(self.cnt)

    def shiftUpward(self, cnt):
        while cnt > 1 and priorityComparision(self.heap_data[int(cnt / 2) - 1],">",self.heap_data[cnt - 1], self.largerGFirst):
            self.heap_data[int(cnt / 2) - 1],self.heap_data[cnt - 1] = self.heap_data[cnt - 1], self.heap_data[int(cnt / 2) - 1]
            cnt = int(cnt / 2)

    def peek(self):
        return self.heap_data[0]

    def pop(self):
        if self.cnt > 0:
            retu = self.heap_data[0]
            self.heap_data[0], self.heap_data[self.cnt - 1] = self.heap_data[self.cnt - 1], self.heap_data[0]
            self.heap_data.pop()
            self.cnt -= 1
            self.shiftDownward(1)
            return retu

    def remove(self, cell_state):
        if self.heap_data.index(cell_state) == 0:
            self.pop()
            return True
        else:
            if self.cnt > 0:
                while cell_state in self.heap_data:
                    state_index = self.heap_data.index(cell_state)
                    self.heap_data[state_index], self.heap_data[self.cnt - 1] = self.heap_data[self.cnt - 1], self.heap_data[state_index]
                    del (self.heap_data[self.cnt - 1])
                    self.cnt -= 1
                    self.shiftDownward(state_index + 1)
            else:
                return False

    def shiftDownward(self, cnt):
        # Move state down to a proper location by priority to maintain the MinStateHeap
        while 2 * cnt <= self.cnt:
            # browse children
            j = 2 * cnt
            if j+1 <= self.cnt:
                if priorityComparision(self.heap_data[j], "<", self.heap_data[j - 1], self.largerGFirst):
                    j += 1
            if priorityComparision(self.heap_data[cnt - 1], "<=", self.heap_data[j - 1], self.largerGFirst):
                break
            self.heap_data[cnt - 1], self.heap_data[j - 1] = self.heap_data[j - 1], self.heap_data[cnt - 1]
            cnt = j

    def toString(self):
        res = "["
        for i in range(len(self.heap_data)):
            res += ("%d: %s" % (smallerGPriority(self.heap_data[i]), self.heap_data[i].loc))
            if i != len(self.heap_data) - 1:
                res += ", "
        res += "]"
        return res

    def contains(self, state: cellState):
        if state in self.heap_data:
            return True
        else:
            return False
