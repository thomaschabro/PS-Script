%{
#include "bison.tab.h"
%}

%%

"setup"         { return SETUP; }
"next"          { return NEXT; }
"plus"          { return PLUS_EQUAL; }
"minus"         { return MINUS_EQUAL; }
"display"       { return DISPLAY; }
"during_race"   { return DURING_RACE; }
"verify"        { return VERIFY; }
"other"         { return OTHER; }
"end_race"      { return END_RACE; }
"end_vef"       { return END_VEF; }
"end_other"     { return END_OTHER; }
"concat"        { return CONCAT; }
"then"          { return THEN; }
"is"            { return IS; }
"track_day"     { return TRACKDAY; }
"end_trackday"  { return END_TRACKDAY; }
"insert"        { return INSERT; }

"<"  { return LESS_THAN; }
">"  { return GREATER_THAN; }
"<=" { return LESS_THAN_EQUAL; }
">=" { return GREATER_THAN_EQUAL; }
"==" { return EQUAL; }
"!=" { return NOT_EQUAL; }

"("  { return LPAREN; }
")"  { return RPAREN; }

":"  { return COLON; }

"+"  { return PLUS; }
"-"  { return MINUS; }
"*"  { return TIMES; }
"/"  { return DIVIDE; }

[0-9]+                 { yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return IDENTIFIER; }
\"(\\.|[^\"\n])*\"     { yylval.str = strdup(yytext); return STRING; }

\n { return NEWLINE; }
[\t\r] { /* ignore whitespace */ }
[ ]+  { /* ignora espacos*/}

. { printf("Unknown character: %s\n", yytext); return yytext[0] ; }
%%