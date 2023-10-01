from .minienv import BasicEnvironment, SpecialBuiltins

'''
Helpers
'''
def list_assign(L, indicies, value):
    if len(indicies) == 1:
        L[indicies.pop(0)] = value
    else:
        U = L
        while len(indicies) > 1:
            U = L[indicies.pop(0)]
        U[indicies.pop(0)] = value

'''
Abstract class for our ASTs
'''
# forward decls
class AST:
    pass

class NumberAST:
    pass

class BinOpAST:
    pass


class AST:
    def emit(self, env):
        pass

class UnaryAST(AST):
    def __init__(self, op : str, value : NumberAST):
        self.op = op
        self.value = value

    def emit(self, env):
        if self.op == '+':
            return self.value.emit(env)
        elif self.op == '-':
            return -self.value.emit(env)

class BinopAST(AST):
    def __init__(self, op: int | float | str, o1 : BinOpAST, o2 : BinOpAST):
        self.op = op
        self.o1 = o1
        self.o2 = o2
    
    def emit(self, env):
        return env[self.op](
            self.o1.emit(env),
            self.o2.emit(env)
        )

class ValueAST(AST):
    def __init__(self, value : int | float | str | list):
        self.value = value
    
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
    
class CodeBlockAST(AST):
    def __init__(self, parts : list[AST]):
        self.parts = parts

    def emit(self, env):
        for part in self.parts:
            if isinstance(part, IfElseAST) or isinstance(part, WhileAST) or isinstance(part, CodeBlockAST):
                val = part.emit(env)
                if val is not None: # this was a return statement
                    return val
            elif isinstance(part, ReturnAST):
                return part.emit(env)
            elif isinstance(part, AssignmentAST):
                if part.symbol in BasicEnvironment.keys():
                    part.emit(BasicEnvironment)
                else:
                    part.emit(env)
            elif isinstance(part, FuncCallAST): # procedure
                part.emit(env)

class FuncdefAST(AST):
    def __init__(self, funcname : str, argnames : list[str], codeblock : list[AST]):
        self.funcname = funcname
        self.argnames = argnames
        self.codeblock = codeblock

    @property
    def ismain(self):
        return self.funcname == 'main'
    
    def emit(self, env):
        env[self.funcname] = self
        return self

class FuncCallAST(AST):
    def __init__(self, funcname : str, argvals : list[AST]):
        self.funcname = funcname
        self.argvals = argvals
    
    def bound_args(self, env):
        func = env[self.funcname]
        return dict(zip(func.argnames, self.argvals))

    def emit(self, env):
        # special case for print
        # XXX bit of a hack
        if self.funcname in SpecialBuiltins.keys():
            return SpecialBuiltins[self.funcname](*[v.emit(env) for v in self.argvals])

        tmpenv = env.copy()
        
        func = tmpenv[self.funcname]

        # bind arguments to temporary environment
        for argname, argexpr in self.bound_args(tmpenv).items():
            tmpenv[argname] = argexpr.emit(tmpenv)

        return func.codeblock.emit(tmpenv)

class ReturnAST(AST):
    def __init__(self, expr):
        self.expr = expr
    
    def emit(self, env):
        return self.expr.emit(env)

class IdentAST(AST):
    def __init__(self, name, subscript_list=[]):
        self.name = name
        self.subscript_list = subscript_list
    
    def emit(self, env):
        # Chose the right environment
        E = env
        if self.name in BasicEnvironment.keys():
            E = BasicEnvironment
        # If we have subscripts, get the indexed value
        if self.subscript_list != []:
            subscripts = self.subscript_list.copy()
            value = E[self.name]
            while subscripts:
                value = value[subscripts.pop(0).emit(env)]
            return value
        # No subscripts
        return E[self.name]
    
class AssignmentAST(AST):
    def __init__(self, ident, expr):
        self.ident  = ident
        self.symbol = ident.name
        self.expr = expr
    
    def emit(self, env):
        if len(self.ident.subscript_list) >= 1:
            slist = [s.emit(env) for s in self.ident.subscript_list]
            value = self.expr.emit(env)
            list_assign(env[self.symbol], slist, value)
        else:
            env[self.symbol] = self.expr.emit(env)
        return env[self.symbol]
        
class IfElseAST(AST):
    def __init__(self, cond : AST, ifblock : list[AST], elseblock : list[AST]):
        self.cond = cond
        self.ifblock = ifblock
        self.elseblock = elseblock

    def emit(self, env):
        if self.cond.emit(env):
            return self.ifblock.emit(env)
        return self.elseblock.emit(env)
    
class WhileAST(AST):
    def __init__(self, cond, codeblock):
        self.cond = cond
        self.codeblock = codeblock

    def emit(self, env):
        while self.cond.emit(env):
            v = self.codeblock.emit(env)
            if v is not None:
                return v

class ProgramAST(AST):
    def __init__(self, preprog : list[AST], mainfunc : FuncdefAST):
        self.preprog = preprog
        self.mainfunc = mainfunc
    
    def emit(self, env=None):
        # emit the preprog and return the mainfunc
        for preprog_block in self.preprog:
            preprog_block.emit(BasicEnvironment)
        self.mainfunc.emit(BasicEnvironment)
        return lambda: FuncCallAST('main', []).emit(BasicEnvironment)