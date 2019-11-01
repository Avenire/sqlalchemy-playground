# What is this sh*t?
Just some experiments I did for educational purposes with pytest and sqlalchemy.

Main goals were to check if I can easily make a 
`column_property` computing multiple aggregates from joined children table
(using postgres json).
Also wondered if I can make integration tests with different db setup
 (no commits, rollbacks & single db per pytest run and single db per test to which they would commit to for real).
 Also checked if can reuse fixture implementation easily (different scopes for different tests).
 
