%{
#include "bison.tab.h"
%}

%%

"setup"         { printf("DEBUG: RETURNING SETUP\n"); return SETUP; }
"next"          { printf("DEBUG: RETURNING NEXT\n"); return NEXT; }
"plus"          { return PLUS; }
"minus"         { return MINUS; }
"display"       { return DISPLAY; }
"during_race"   { printf("DEBUG: RETURNING WHILE\n"); return DURING_RACE; }
"verify"        { return VERIFY; }
"other"         { return OTHER; }
"end_race"      { return END_RACE; }
"end_vef"       { return END_VEF; }
"end_other"     { return END_OTHER; }
"concat"        { return CONCAT; }
"then"          { return THEN; }
"is"            { return IS; }
"track_day"     { printf("DEBUG: RETURNING TRACKDAY\n"); return TRACKDAY; }
"end_trackday"  { printf("DEBUG: RETURNING END_TRACKDAY\n"); return END_TRACKDAY; }

"<"  { return LESS_THAN; }
">"  { return GREATER_THAN; }
"<=" { return LESS_THAN_EQUAL; }
">=" { return GREATER_THAN_EQUAL; }
"==" { return EQUAL; }
"!=" { return NOT_EQUAL; }

"("  { return LPAREN; }
")"  { printf("DEBUG: RETURNING RPAREN\n"); return RPAREN; }

":"  { return COLON; }

"+"  { return PLUS; }
"-"  { return MINUS; }
"*"  { return TIMES; }
"/"  { return DIVIDE; }
"+=" { return PLUS_EQUAL; }
"-=" { return MINUS_EQUAL; }

[0-9]+                 { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return IDENTIFIER; }
\"(\\.|[^\"\n])*\"     { yylval.str = strdup(yytext); return STRING; }

\n { return NEWLINE; }
[\t\r] { /* ignore whitespace */ }
[ ]+  { /* ignora espacos*/}

. { printf("Unknown character: %s\n", yytext); return yytext[0] ; }
%%