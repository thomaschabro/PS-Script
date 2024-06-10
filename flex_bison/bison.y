%{
#include <stdio.h>
extern int yylex();
extern FILE *yyin;
void yyerror(const char *);
%}

%union {
    char* str;
    int num;
}

%token SETUP NEXT DISPLAY DURING_RACE VERIFY OTHER END_RACE END_VEF END_OTHER CONCAT THEN IS TRACKDAY END_TRACKDAY IDENTIFIER STRING INSERT
%token <num> NUMBER
%token LESS_THAN GREATER_THAN LESS_THAN_EQUAL GREATER_THAN_EQUAL EQUAL NOT_EQUAL LPAREN RPAREN COLON PLUS MINUS TIMES DIVIDE PLUS_EQUAL MINUS_EQUAL NEWLINE

%type <num> expression

%%

block: TRACKDAY NEWLINE statements END_TRACKDAY
        ;

statements:
        | statements statement

statement: declaration NEWLINE | assignment NEWLINE | display NEWLINE | during NEWLINE | vef NEWLINE | NEWLINE
        ;

declaration: SETUP IDENTIFIER set_opt
        ;

assignment: IDENTIFIER ass_aux
        ;

ass_aux: define | increment | plus_opt | minus_opt

set_opt:
        | define
        ;

define: IS define_aux
        ;

define_aux: expression | insert_opt
        ;

insert_opt: INSERT LPAREN RPAREN
        ;

increment: NEXT
        ;

plus_opt: PLUS_EQUAL expression
        ;

minus_opt: MINUS_EQUAL expression
        ;

display: DISPLAY LPAREN str_exp concat_loop RPAREN
        ;

str_exp: STRING | expression
        ;

concat_loop:
        | CONCAT str_exp concat_loop
        ;

during: DURING_RACE LPAREN expression comparator expression RPAREN NEWLINE statements END_RACE
        ;

vef: VERIFY LPAREN expression comparator expression RPAREN THEN COLON NEWLINE statements END_VEF other_opt
        ;

other_opt:
        | NEWLINE OTHER COLON NEWLINE statements END_OTHER
        ;

expression: term exp_aux
        ;

exp_aux:
        | plus_minus term exp_aux
        ;

plus_minus: PLUS | MINUS
        ;

term : factor term_aux
        ;

term_aux:
        | times_div factor term_aux
        ;

times_div: TIMES | DIVIDE
        ;

factor: PLUS factor | MINUS factor | NUMBER | IDENTIFIER | LPAREN expression RPAREN
        ;

comparator: LESS_THAN | GREATER_THAN | LESS_THAN_EQUAL | GREATER_THAN_EQUAL | EQUAL | NOT_EQUAL
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