# SimpleInterpreter
A simple interpreter written in Python inspired by http://www.craftinginterpreters.com/

It can currently interpret a simple procedural language. The language consists of integer, float, boolean and string variables, arithmetic and logical operations as well as string concatenation, assignment, control structures, and functions. A sample program follows:

```
fun factorial(x) {
    result := 1

    if x < 0 {
        ret -1
    } else {
        while x > 0 {
            result := result * x
            x := x - 1
        }
        ret result
    }
}

print('7! - 2 = ' # factorial(7) - 2)

fun facrec(x) {
    if x = 0 {
        ret 1
    } else {
        ret facrec(x-1) * x
    }
}

print(facrec(7))
first_part := 'Recursive and iterative computes the same is a __'
print(first_part # facrec(4) = factorial(4) # '__ statement.')


fun calcPi(num_iter) {
    pi := 0
    fun aux(nominator, even, iter) {
        if iter = num_iter {
            ret 4*pi
        }
        if even {
            value := -1/nominator
        } else {
            value := 1/nominator
        }
        pi := pi + value
        ret aux(nominator+2, not even, iter+1)
    }
    ret aux(1, false, 1)
}

print('Pi is approximately: ' # calcPi(100))

```
