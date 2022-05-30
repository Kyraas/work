# https://webdevblog.ru/sozdanie-konechnyh-avtomatov-s-pomoshhju-korutin-v-python/

def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class RegexFSM:
    def __init__(self):
        self.start = self._create_start()
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()
        self.q3 = self._create_q3()
        
        self.current_state = self.start
        self.stopped = False
        
    def send(self, char):
        try:
            print(char)
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True
        
    def does_match(self):
        if self.stopped:
            return False
        return self.current_state == self.q3

    @prime
    def _create_start(self):
        while True:
            char = yield
            if char == 'a':
                self.current_state = self.q1
            else:
                break
    
    @prime
    def _create_q1(self):
        while True:
            # Подождем, пока ввод не будет получен.
            # после получения сохраним ввод в char
            char = yield
            if char == 'b':
                # при получении b состояние перемещается в q2
                self.current_state = self.q2
            elif char == 'c':
                # при получении c состояние перемещается в q3
                self.current_state = self.q3
            else:
                # при получении любого другого ввода, разорвать петлю
                # чтобы в следующий раз, когда кто-нибудь отправит
                # корутину вызываем StopIteration
                break

    @prime
    def _create_q2(self):
        while True:
            char = yield
            if char == 'b':
                self.current_state = self.q2
            elif char == 'c':
                self.current_state = self.q3
            else:
                break

    @prime
    def _create_q3(self):
        while True:
            char = yield
            break


def grep_regex(text):
    evaluator = RegexFSM()
    for ch in text:
        evaluator.send(ch)
    return print(evaluator.does_match())

# grep_regex("a")
# grep_regex("ab")
# grep_regex("ac")
# grep_regex("abc")
# grep_regex("aba")
# grep_regex("abbbbbbbc")
# grep_regex("abcc")
# grep_regex("abcd")
grep_regex("bcbc")
