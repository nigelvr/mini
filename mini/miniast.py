from .minienv import BasicEnvironment

def emit_funcbody(funcbody : list, env):
    for funcpart in funcbody:
        if isinstance(funcpart, ReturnAST):
            return funcpart.emit(env)
        elif isinstance(funcpart, IfAST) or isinstance(funcpart, WhileAST):
            val = funcpart.emit(env)
            if val is not None: # this was a return statement
                return val
        elif isinstance(funcpart, AssignmentAST):
            if funcpart.symbol in BasicEnvironment.keys():
                funcpart.emit(BasicEnvironment)
            else:
                funcpart.emit(env)
        elif isinstance(funcpart, FuncCallAST): # procedure
            funcpart.emit(env)

def list_assign(L, indicies, value):
    if len(indicies) == 1:
        L[indicies.pop(0)] = value
    else:
        U = L
        while len(indicies) > 1:
            U = L[indicies.pop(0)]
        U[indicies.pop(0)] = value


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

class ValueAST(AST):
    def __init__(self, val):
        super().__init__(val, [])
    
    @property
    def value(self):
        return self.root
    
    def emit(self, env=None):
        return self.value
    
class NumberAST(ValueAST):
    def emit(self, env=None):
        return self.value

class ListAST(ValueAST):
    def emit(self, env=None):
        L = []
        for l in self.value:
            L.append(l.emit(env))
        return L
    
    def access(self, idx, env=None):
        return self.value[idx].emit(env)
    
class FuncdefAST(AST):
    def __init__(self, funcname, argnamelist, funcbody):
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
        tmpenv = env.copy()
        
        func = tmpenv[self.funcname]

        # bind arguments to temporary environment
        for argname, argexpr in self.bound_args(tmpenv).items():
            tmpenv[argname] = argexpr.emit(tmpenv)

        return emit_funcbody(func.funcbody, tmpenv)

class ReturnAST(AST):
    def __init__(self, expr):
        super().__init__(expr, [])

    @property
    def expr(self):
        return self.root
    
    def emit(self, env):
        return self.root.emit(env)

class IdentAST(AST):
    def __init__(self, ident, subscript_list=[]):
        super().__init__(ident, subscript_list)

    @property
    def name(self):
        return self.root

    @property
    def subscript_list(self):
        return self.children
    
    def emit(self, env):
        # Chose the right environment
        E = env
        if self.root in BasicEnvironment.keys():
            E = BasicEnvironment
        # If we have subscripts, get the indexed value
        if self.subscript_list != []:
            subscripts = self.subscript_list.copy()
            value = E[self.root]
            while subscripts:
                value = value[subscripts.pop(0).emit(env)]
            return value
        # No subscripts
        return E[self.root]
    
class AssignmentAST(AST):
    def __init__(self, ident, expr):
        super().__init__(ident, [expr])

    @property
    def symbol(self):
        return self.root.name
    
    def emit(self, env):
        if len(self.root.subscript_list) >= 1:
            slist = [s.emit(env) for s in self.root.subscript_list]
            value = self.children[0].emit(env)
            list_assign(env[self.symbol], slist, value)
        else:
            env[self.symbol] = self.children[0].emit(env)
        return env[self.symbol]
    
class FPartAST(AST):
    def __init__(self, cond, body):
        super().__init__(cond, body)
    
    @property
    def cond(self):
        return self.root
    
    @property
    def body(self):
        return self.children
        
class IfAST(FPartAST):
    def emit(self, env):
        if self.cond.emit(env):
            return emit_funcbody(self.body, env)
        
class WhileAST(FPartAST):
    def emit(self, env):
        while self.cond.emit(env):
            v = emit_funcbody(self.body, env)
            if v is not None:
                return v
