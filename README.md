# interpreter for mini imperative programming language

I used the ply (python lex-yacc) library for constructing the lexer and parser.

Some examples:

Fibonacci and factorial

```
func fib(n) {
    if (n == 0 or n == 1) {
        return 1;
    }
    return fib(n-1) + fib(n-2);
}

func fact(n) {
    if (n == 0) {
        return 1;
    }
    return n * fact(n-1);
}


# Main function
func main() {
    return fib(5) + fact(5);
}
```

Bubble sort
```
func main() {
    L = [3, 5, 6, 1, 2, 7];
    i = 0;
    j = 0;
    while (i < 6) {
        j = i+1;
        while (j < 6) {
            if (L[i] > L[j]) {
                tmp = L[i];
                L[i] = L[j];
                L[j] = tmp;
            }
            j = j+1;
        }
        i = i+1;
    }
    return L;
}
```
