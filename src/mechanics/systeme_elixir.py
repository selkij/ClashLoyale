MAX_ELIXIR = 10
START_ELIXIR = 5
SINGLE_ELIXIR_DURATION = 120
DOUBLE_ELIXIR_DURATION = 60
ELIXIR_SECONDS = 2.8


class ElixirSystem:
    def __init__(self):
        self.elapsed_time = 0
        self.multiplier = 1

    def reset(self):
        self.elapsed_time = 0
        self.multiplier = 1

    def update(self, dt, players):
        self.elapsed_time += dt
        self.multiplier = self.get_multiplier()
        amount = self.multiplier / ELIXIR_SECONDS * dt

        for player in players:
            player.modify_elixir(amount, log_change=False)

    def get_multiplier(self):
        if self.elapsed_time < SINGLE_ELIXIR_DURATION:
            return 1
        if self.elapsed_time < SINGLE_ELIXIR_DURATION + DOUBLE_ELIXIR_DURATION:
            return 2
        return 3
