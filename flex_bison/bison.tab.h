/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_BISON_TAB_H_INCLUDED
# define YY_YY_BISON_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    SETUP = 258,                   /* SETUP  */
    NEXT = 259,                    /* NEXT  */
    DISPLAY = 260,                 /* DISPLAY  */
    DURING_RACE = 261,             /* DURING_RACE  */
    VERIFY = 262,                  /* VERIFY  */
    OTHER = 263,                   /* OTHER  */
    END_RACE = 264,                /* END_RACE  */
    END_VEF = 265,                 /* END_VEF  */
    END_OTHER = 266,               /* END_OTHER  */
    CONCAT = 267,                  /* CONCAT  */
    THEN = 268,                    /* THEN  */
    IS = 269,                      /* IS  */
    LESS_THAN = 270,               /* LESS_THAN  */
    GREATER_THAN = 271,            /* GREATER_THAN  */
    LESS_THAN_EQUAL = 272,         /* LESS_THAN_EQUAL  */
    GREATER_THAN_EQUAL = 273,      /* GREATER_THAN_EQUAL  */
    EQUAL = 274,                   /* EQUAL  */
    NOT_EQUAL = 275,               /* NOT_EQUAL  */
    LPAREN = 276,                  /* LPAREN  */
    RPAREN = 277,                  /* RPAREN  */
    COLON = 278,                   /* COLON  */
    PLUS = 279,                    /* PLUS  */
    MINUS = 280,                   /* MINUS  */
    TIMES = 281,                   /* TIMES  */
    DIVIDE = 282,                  /* DIVIDE  */
    PLUS_EQUAL = 283,              /* PLUS_EQUAL  */
    MINUS_EQUAL = 284,             /* MINUS_EQUAL  */
    NEWLINE = 285                  /* NEWLINE  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_BISON_TAB_H_INCLUDED  */
