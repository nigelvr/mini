class AST:
    def __init__(self, root, children):
        self.root = root
        self.children = children

    def emit(self, env):
        pass

class UnaryAST(AST):
    def __init__(self, op, value):
        super().__init__(op, [value])

    @property
    def op(self):
        return self.root
    
    @property
    def value(self):
        return self.children[0]

    def emit(self, env):
        if self.op == '+':
            return self.value.emit(env)
        elif self.op == '-':
            return -self.value.emit(env)

class BinopAST(AST):
    def __init__(self, op, p1, p2):
        super().__init__(op, [p1, p2])
    
    @property
    def op(self):
        return self.root
    
    @property
    def o1(self):
        return self.children[0]
    
    @property
    def o2(self):
        return self.children[1]
    
    def emit(self, env):
        return env[self.op](
            self.o1.emit(env),
            self.o2.emit(env)
        )

class NumberAST(AST):
    def __init__(self, number):
        super().__init__(number, [])

    def negate(self):
        self.root *= -1
        return self
    
    @property
    def value(self):
        return self.root
    
    def emit(self, env=None):
        return self.value
    
class FuncdefAST(AST):
    def __init__(self, funcname, argnamelist, funcbody):
        print(f'FuncdefAST : funcname={funcname}, argnamelist={argnamelist}, funcbody={funcbody}')
        super().__init__(funcname, [argnamelist, funcbody])
    
    @property
    def funcname(self):
        return self.root
    
    @property
    def argnamelist(self):
        return self.children[0]
    
    @property
    def funcbody(self):
        return self.children[1]
    
    def emit(self, env):
        env[self.funcname] = self
        return self

class FuncCallAST(AST):
    def __init__(self, funcname, arglist):
        print(f'FuncCallAST: funcname={funcname}, arglist={arglist}')
        super().__init__(funcname, arglist)

    @property
    def funcname(self):
        return self.root
    
    @property
    def arglist(self):
        return self.children
    
    def bound_args(self, env):
        func = env[self.funcname]
        return dict(zip(func.argnamelist, self.arglist))

    def emit(self, env):
        func = env[self.funcname]
        retval = None

        # bind arguments
        for argname, argexpr in self.bound_args(env).items():
            env[argname] = argexpr.emit(env)

        # compute
        if func.funcbody is not None:
            retval = func.funcbody.emit(env)

        # unbind arguments
        for argname, _ in self.bound_args(env).items():
            env.pop(argname)

        return retval

class ReturnAST(AST):
    def __init__(self, expr):
        super().__init__(expr, [])

    @property
    def expr(self):
        return self.root
    
    def emit(self, env):
        return self.root.emit(env)

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