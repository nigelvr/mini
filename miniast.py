class AST:
    def __init__(self, root, children):
        self.root = root
        self.children = children

    def emit(self, env):
        pass

class UnaryAST(AST):
    def __init__(self, op, value):
        super().__init__(op, [value])

    def emit(self, env):
        if self.root == '+':
            return self.children[0].emit(env)
        elif self.root == '-':
            return -self.children[0].emit(env)

class BinopAST(AST):
    def __init__(self, op, p1, p2):
        super().__init__(op, [p1, p2])
    
    def emit(self, env):
        return env[self.root](
            self.children[0].emit(env),
            self.children[1].emit(env)
        )

class NumberAST(AST):
    def __init__(self, number):
        super().__init__(number, [])

    def negate(self):
        self.root *= -1
        return self
    
    def emit(self, env=None):
        return self.root
    
class FuncdefAST(AST):
    def __init__(self, funcname, argname, expr):
        super().__init__(funcname, [argname, expr])

    def emit(self, env):
        env[self.root] = self
        return self

class FuncCallAST(AST):
    def __init__(self, funcname, argvalue):
        super().__init__(funcname, [argvalue])

    def emit(self, env):
        func = env[self.root]
        argname = func.children[0]
        # bind, get value, unbind
        # print(f'argname {argname}')
        env[argname] = self.children[0].emit(env)
        val = func.children[1].emit(env)
        env.pop(argname)
        return val

class IdentAST(AST):
    def __init__(self, ident):
        super().__init__(ident, [])
    
    def emit(self, env):
        return env[self.root]
    
class AssignmentAST(AST):
    def __init__(self, ident, expr):
        super().__init__(ident, [expr])
    
    def emit(self, env):
        env[self.root] = self.children[0].emit(env)
        return env[self.root]