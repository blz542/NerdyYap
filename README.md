# NerdyYap

NerdyYap is a programming language made by BLZ542, specifically built to be an esolang made not to make coding easier, but fun. It uses Gen Z terminology and slangs as part of its syntax, giving traditional programming concepts a twist while still functioning as a real programming language.


The CLI command is nerd:  nerd program.nerd

## Syntax

Comments are used the same way as in Python, by using `#`

Variables:
`yo x be 10;`

Strings:
`yo name be "NerdyYap";`

Characters use single quotes and contain exactly one character:
`yo initial be 'N';`

Output:
`yap "Hello, world!";`
`yap x;`

Arithmetic:
`yo result be 10 + 5 * 2;`

Supports `+`, `-`, `*`, `/`, and parentheses.

Arrays:
`yo nums be [10, 20, 30];`
`yap nums[0];`
`yo nums[0] be 99;`

Arrays can contain numbers, strings, characters. Array methods and nested arrays are not supported yet.

Comparisons:
`mogs` = `>`
`gets mogged by` = `<`
`larping` = `==`

If / Else:
```nerd
if x gets mogged by y {
    yap "X GOT COOKED";
} else {
    yap "X MOGS Y";
}

Loops and control flow:

while x gets mogged by 10 {
    yap x;
    yo x be x + 1;
}

grind {
    yap "runs at least once";
} while x mogs 0;

for item in nums {
    yap item;
}

break;
continue;

