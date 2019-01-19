# SimpleInterpreter
A simple interpreter written in Python inspired by http://www.craftinginterpreters.com/

It can currently interpret a very simple language consisting of integer and boolean variables, arithmetic and boolean expressions,
assignment and control structures. A sample program to calculate the factorial of a number follows:

```
x := 7
result := 1
doCompute := 1

if x < 0 or not (doCompute = 1) {
    print -1
} else {
    while x > 0 {
        result := result * x
        x := x - 1
    }
    print result
}

```
