# PS-Script
PSS (Pit Stop Script) é uma linguagem de programação voltada para o meio automobilístico. Nela, engenheiros de equipes da F1 podem inserir as informações dos carros competidores, para então poder simular uma corrida. 

## EBNF 
```
BLOCK = { STATEMENT };
STATEMENT = ( "λ" | DECLARATION | ASSIGNMENT | DISPLAY | DURING_RACE | VERIFY ), "\n";

DECLARATION = "setup", IDENTIFIER, [SET];
ASSIGNMENT = IDENTIFIER, ( SET | INCREMENT | PLUS | MINUS ) ;

SET = "is", EXPRESSION;

INCREMENT = "next";

PLUS = "plus", EXPRESSION;
MINUS = "minus", EXPRESSION;

DISPLAY = "display", "(", ( STRING | EXPRESSION ), {"concat", ( STRING | EXPRESSION ) }, ")";

DURING_RACE = "during_race", "(", EXPRESSION, COMPARATOR, EXPRESSION, ")", "\n", { STATEMENT }, "end_race";

VERIFY = "verify", "(", EXPRESSION, COMPARATOR, EXPRESSION, ")", "then", ":", "\n", { STATEMENT }, "end_vef", [OTHER];

OTHER = "other", ":", "\n", { STATEMENT }, "end_other";

EXPRESSION = TERM, { ("+" | "-"), TERM };
TERM = FACTOR, { ("*" | "/"), FACTOR };
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" };
NUMBER = DIGIT, { DIGIT };
LETTER = ( "a" | "..." | "z" | "A" | "..." | "Z" );
DIGIT = ( "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" );
COMPARATOR = ( "<" | ">" | "<=" | ">=" | "==" | "!=" );
STRING = '"' { "λ" | LETTER | DIGIT } '"'
```
## Código de exemplo
```
setup track_size is 500
setup n_laps is 20

setup lap
lap is 0

setup car_max_vel is insert()
setup car_lap_acceleration is insert()

setup vel is 0
setup time_lap is 0
setup time_total is 0

during_race (lap < n_laps)
	lap next
	
	verify (vel == car_max_vel) then:
		display("Car in max speed")
	end_vef
	other:
		vel plus car_lap_acceleration
	end_other

	time_lap is track_size / vel
	time_total plus time_lap
end_race

display("Total time was " concat time_total)
```

