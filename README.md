# Derby-Derp

A small, terminal-based horse betting championship game written in Python. Bet on randomized horses across a multi-race championship while managing stamina, injuries, weather, obstacles and power-ups.

---

## Table of Contents

- [Quick start](#quick-start)
- [Play](#play)
- [Gameplay summary](#gameplay-summary)
- [Controls](#controls)
- [Configuration](#configuration)
- [Extending / Development notes](#extending--development-notes)
- [Tips & balancing](#tips--balancing)
- [License](#license)
- [Author](#author)

---

## Quick start

Requirements
- Python 3.7+

Clone and run:

```bash
git clone https://github.com/DoodleSaurus/Derby-Derp.git
cd Derby-Derp
python3 horsebet.py   # or `python horsebet.py` on Windows
```

Default values
- Starting balance: $100
- Championship length: 5 races
- Number of horses: 5

---

## Play

1. Start the script.
2. Enter your bet when prompted (integer). Enter `0` to quit.
3. Choose a horse number from the displayed list (only healthy horses are shown).
4. Watch the terminal race animation and see results.

Example session:

```
Enter your bet amount (or 0 to quit): 10
Available horses:
1. Thunder Blaze (Stamina: 100%)
2. Midnight Rider (Stamina: 95%)
3. Lightning Flash (Stamina: 88%)
Choose a horse to bet on: 2
# ...race runs...
Midnight Rider wins the race! You won $20!
```

Payouts
- Win: 2× your bet (you receive your bet back plus winnings equal to bet)
- Loss: you lose the bet amount

---

## Gameplay summary

- Stamina (0–100): impacts movement; low stamina reduces speed and increases injury chance.
- Injuries: force a horse to miss a number of races.
- Weather: randomly selected each race — affects all horses with a speed multiplier.
- Obstacles: chance events that may slow a horse (mud patch, hurdle, etc.).
- Power-ups: chance events that may boost a horse (energy boost, lucky horseshoe, etc.).
- Championship: top 5 finishers earn points each race (default: 10, 6, 4, 2, 1). After the last race a champion is declared and a small player bonus is awarded.

---

## Controls

- When prompted, enter integer values for bet amounts and horse choices.
- Enter `0` at the bet prompt to quit.
- Use Ctrl+C to interrupt the game immediately.

---

## Configuration

Most defaults are easy to edit inside `horsebet.py`:

- Championship length:
```python
championship = Championship(num_races=5)
```

- Horse count:
```python
horses = [Horse(i+1) for i in range(5)]
```

- Weather and effects: modify `WEATHER_TYPES` and `WEATHER_EFFECTS`.
- Obstacles and power-ups: edit `OBSTACLES` and `POWER_UPS`.
- Starting balance and movement/stamina numbers are defined in the `main()` loop and `Horse` methods.

If you want command-line options, consider adding argparse to expose these parameters.

---

## Extending / Development notes

- Race logic is in `race_animation()` — movement is calculated from a random base move, stamina fraction, and weather multiplier. Obstacles and power-ups are applied per tick.
- Horse lifecycle (stamina, injury, rest, stats) is in the `Horse` class.
- Championship scoring is in the `Championship` class.
- To add unique horse stats (speed, consistency), add attributes to `Horse` and include them in movement calculations.
- Persisting player profiles or leaderboards can be done with a JSON file (simple read/write).

---

## Tips & balancing

- Reduce per-race stamina drain to make races less punishing.
- Tweak power-up/obstacle chances for different difficulty levels.
- Increase variety by adding more weather types or per-horse traits.

---

## License

Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)

You may share this work (including commercially) but you may not distribute modified versions. Attribution is required. See the `LICENSE` file or https://creativecommons.org/licenses/by-nd/4.0/ for full text.

---

Have fun, and may the best horse win!
