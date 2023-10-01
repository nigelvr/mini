from mini.runner import run

if __name__ == '__main__':
    prog = '''
    func main() {
        if (1 < 10) {
            return 2;
        }
        return 1;
    }
    '''
    result = run(prog)
    print(result)