## Introduction

IMP is a simple, minimal programming language. It was taught to me in
a class in grad school on proving semantics of programming
languages. I decided to write a simple interpreter for it as a running
example in a
[series of blog posts on building interpreters](https://jayconrod.com/tags/imp).

## The language

IMP programs have three syntactic entities:

* Statements
* Arithmetic expressions (aexps)
* Boolean expressions (bexps)

A program consists of a single statement, but statements can contain
other statements. Arithmetic expressions are simple expressions that
evaluate to integers. Boolean expressions evaluate to true or
false. There are no values, other than integers and Booleans.

Variables may be assigned in IMP. All variables are global. There are
no functions or scopes, so non-global variables wouldn't really make
sense anyway. When an IMP program is finished executing, the
interpreter prints the value of each variable. There is no other way
for IMP programs to interact with the outside world.

### Statements

* Assignment statement: sets a variable to an integer obtained by
evaluating an aexp.

```
x := 1 + 2
```

* Compound statement: two sub-statements, separated by a
semicolon. Multiple statements may be chained together with this.

```
x := 1;
y := 2;
z := 3
```

* If statement: a bexp condition and two sub-statements, separated by
`else`. If the condition evaluates to `true`, the first statement is
executed. Otherwise, the second statement is executed.

```
if a < b then
  x := 1
else
  y := 2
end
```

* While statement: a bexp condition and a loop body sub-statement. If
the condition evaluates to `true`, the loop body is executed. This is
repeated until the condition evaluates to `false`.

```
while x > 0 do
  x := x - 1
end
```

### Arithmetic expressions (aexps)

* Integer literal expression: just an integer that evaluates to
itself.

```
1234
```

* Variable expression: evaluates to the current value of a
variable. If the variable has not been assign, evaluates to 0.

```
x
```

* Binary operator expression: performs an arithmetic operation
(`+`, `-`, `*`, `/`) on two sub-aexps.

```
12 + x
```

### Boolean expressions (bexps)

* Relational operator expression: performs a relational operation
(`<`, `<=`, `>`, `>=`, `=`, `!=`) on two sub-aexps.

```
x < 12
```

* And expression: two sub-bexps separated by `and`. Evaluates to `true`
if both sub-expressions evaluate to true.

```
x < 12 and y < 34
```

* Or expression: two sub-bexps separated by `or`. Evaluates to `true`
if either sub-expression evaluates to true.

```
x < 12 or y < 34
```

* Not expression: a sub-bexp, prefixed by `not`. Evaluates to the
opposite of whatever the sub-expression evaluates to.

```
not x < 12
```

## Structure of the interpreter

TODO: write this section after refactoring.
