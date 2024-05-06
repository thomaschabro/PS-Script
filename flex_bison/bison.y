%{
#include <stdio.h>
extern int yylex();
extern FILE *yyin;
void yyerror(const char *);
%}

%token SETUP NEXT DISPLAY DURING_RACE VERIFY OTHER END_RACE END_VEF END_OTHER CONCAT THEN IS
%token LESS_THAN GREATER_THAN LESS_THAN_EQUAL GREATER_THAN_EQUAL EQUAL NOT_EQUAL LPAREN RPAREN COLON PLUS MINUS TIMES DIVIDE PLUS_EQUAL MINUS_EQUAL  NEWLINE

%%
block: '{' statement '}'
        ;

statement: '(' declaration | assignment | display | during | vef ')' NEWLINE
        ;

declaration: SETUP identifier '[' set_opt ']'
        ;

assignment: identifier '(' set_opt | increment | plus_opt | minus_opt ')'
        ;

set_opt: IS expression
        ;

increment: NEXT
        ;

plus_opt: PLUS_EQUAL expression
        ;

minus_opt: MINUS_EQUAL expression
        ;

display: DISPLAY LPAREN '(' string | expression ')' '{' CONCAT '(' string | expression ')' '}' RPAREN 
        ;

during: DURING_RACE LPAREN expression comparator expression RPAREN NEWLINE block END_RACE
        ;

vef: VERIFY LPAREN expression comparator expression RPAREN THEN COLON NEWLINE block END_VEF '[' other_opt ']'
        ;   

other_opt: OTHER COLON NEWLINE block END_OTHER
        ;

expression: term '{' '(' PLUS | MINUS ')' term '}' 
        ;

term : factor '{' '(' TIMES | DIVIDE ')' factor '}' 
        ;

factor: '(' '(' PLUS | MINUS ')' factor ')' | number | identifier | LPAREN expression RPAREN
        ;

identifier: letter { letter | digit | '_'}
        ;

number: digit '{' digit '}' 
        ;

letter: '(' 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' ')'
        ;

digit: '(' '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ')'
        ;

comparator: LESS_THAN | GREATER_THAN | LESS_THAN_EQUAL | GREATER_THAN_EQUAL | EQUAL | NOT_EQUAL
        ;

string: '"' { letter | digit | ' ' | colon | MINUS | PLUS | '!' | '.' } '"'
        ;

%%
void yyerror(const char *s) {
    fprintf(stderr, "%s\n", s);
}

int main() {
    yyin = stdin;
    yyparse();
    return 0;
}