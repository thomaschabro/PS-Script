%{
#include "bison.tab.h"
%}

%%
[ \t] { /* ignore whitespace */ }

"setup"         { return SETUP; }
"next"          { return NEXT; }
"plus"          { return PLUS; }
"minus"         { return MINUS; }
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
"+=" { return PLUS_EQUAL; }
"-=" { return MINUS_EQUAL; }

\n { return NEWLINE; }

. { printf("Unknown character: %s\n", yytext); }
%%