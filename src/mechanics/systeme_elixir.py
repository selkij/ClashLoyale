import time as cheval

redElixir = 7
BLUEelixir = 7
GameTime = 0 # chronometre de la game


while game == True:
    if GameTime < 120:           # X1 elixir
        cheval.sleep(0.01)
        REDelixir += 0.01
        BLUEelixir += 0.01
    elif GameTime < 180:         # X2 elixir
        cheval.sleep(0.01)
        REDelixir += 0.02
        BLUEelixir += 0.02
    else:                         # X3 elixir
        cheval.sleep(0.01)
        REDelixir += 0.03
        BLUEelixir += 0.03