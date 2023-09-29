import pytest
from mini.runner import run, run_from_path

def test_unary_minus():
    prog = '''
    func main() {
       return -3;
    }
    '''
    assert(run(prog) == -3)

def test_unary_plus():
    prog = '''
    func main() {
       return +3;
    }
    '''
    assert(run(prog) == 3)

def test_global():
    prog = '''
    x = 3;
    func main() {
       return x;
    }
    '''
    assert(run(prog) == 3)

def test_local():
    prog = '''
    func main() {
       x = 3;
       return x;
    }
    '''
    assert(run(prog) == 3)

def test_binop_plus():
    prog = '''
    func main() {
       return 2+3;
    }
    '''
    assert(run(prog) == 5)

def test_binop_minus():
    prog = '''
    func main() {
       return 2-3;
    }
    '''
    assert(run(prog) == -1)

def test_binop_times():
    prog = '''
    func main() {
       return 2*3;
    }
    '''
    assert(run(prog) == 6)

def test_binop_div():
    prog = '''
    func main() {
       return 6/3;
    }
    '''
    assert(run(prog) == 2)

def test_if():
    prog = '''
    func main() {
       x = 5;
       if (x < 10) {
           return 2;
       }
       return 1;
    }
    '''
    assert(run(prog) == 2)
    
def test_while():
    prog = '''
    func main() {
       x = 0;
       y = 0;
       while (x < 5) {
          y = y+2;
          x = x+1;
       }
       return y;
    }
    '''
    assert(run(prog) == 10)

