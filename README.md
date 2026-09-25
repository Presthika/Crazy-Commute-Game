# Crazy Commute

A transportation-themed board game with embedded electronics, built for a real client in Cornerstone of Engineering I at Northeastern University (Fall 2025).

Players pick a mode of transportation and race to pick up the most coworkers on their commute to cities around the world. Along the way, a traffic light, a memory game, and servo-driven obstacles (a bird, a pedestrian, and a railroad crossing) can change the route.

## Design requirements

Our client, a Civil Engineering student, asked for a game that was:
- Themed around transportation
- Competitive and replayable, with more than one way to win
- Portable enough to fit in a backpack

Course constraints: at least three electronic components beyond the class kit, all controlled by a Raspberry Pi Pico, powered from a single plug, with at least one part designed in AutoCAD and laser cut. Budget: $100 over eight weeks.

## Hardware

| Component | Pico pin(s) |
|---|---|
| RGB LED 1 (traffic light) | GP0, GP1, GP2 |
| RGB LED 2 (traffic light) | GP8, GP9, GP10 |
| Red light button | GP5 |
| 5-way switch | GP11 to GP15 |
| Indicator LEDs (x4) | GP16 to GP19 |
| Servo: railroad crossing | GP26 |
| Servo: pedestrian | GP27 |
| Servo: bird | GP28 |

## How the code works

Everything runs in one cooperative loop in `main.py`, with a shared timer that tracks elapsed time across every action.

- **Traffic light:** the RGB LEDs cycle green, yellow, and red. Players can run a red light, but if another player catches them and presses the button, all four LEDs flash and the runner skips a turn.
- **Memory game:** pressing the center of the 5-way switch lights a random 6-step LED sequence. The player repeats it with the switch directions.
- **Obstacles:** a correct sequence flashes the LEDs and lets the player choose a servo obstacle to block another path. Each obstacle resets automatically after 30 seconds. A wrong sequence lights all four LEDs at once.

## Physical build

- Game pieces and coworker tokens laser cut from clear acrylic, designed in AutoCAD
- Cardboard board and electronics box that both fold to a quarter of their size, with wiring laid out to stay connected when folded

## What we would improve

- Mount the 5-way switch more securely and give it a joystick-style cap, since the client found it hard to control
- Keep obstacles active until another player clears them, so games last longer

## Team

Wanderlust Gaming Co.: Molly Herringshaw, Ariba Khan, Jaydon Mac, Presthika Vijaykumar
