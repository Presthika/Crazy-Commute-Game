# Crazy-Commute-Game
Cornerstone of Engineering Class Project

# 🚗 Crazy Commute

A transportation-themed board game with embedded electronics, built for a client as part of Northeastern University's Cornerstone of Engineering I program.

Players race to pick up the most coworkers on their commute to cities around the world — but obstacles like birds, pedestrians, and railroad crossings can block your path.

---

## Hardware

| Component | Pin(s) |
|---|---|
| RGB LED 1 | GP0, GP1, GP2 |
| RGB LED 2 | GP8, GP9, GP10 |
| Speaker | GP7 |
| 5-way switch | GP11–GP15 |
| Regular LEDs (x4) | GP16–GP19 |
| Servo (bird) | GP28 |
| Servo (pedestrian) | GP27 |
| Servo (railroad crossing) | GP26 |
| Red light button | GP5 |

---

## How it works

- **Traffic light** — RGB LEDs cycle green → yellow → red on a timer. Running a red light is allowed but risky — other players can press the button to call you out
- **Memory game** — press the 5-way switch center to generate a random 6-LED sequence. Match it correctly and a victory tune plays; fail and you hear the loss sound
- **Obstacles** — win the memory game to activate a servo that blocks a path on the board (bird, pedestrian, or railroad crossing). Obstacles auto-reset after 30 seconds
- **Physical board** — foldable cardboard game board + laser-cut acrylic game pieces, designed in AutoCAD

---

## Tech Stack

- Raspberry Pi Pico
- MicroPython
- PWM servos (x3)
- RGB LEDs, regular LEDs, passive speaker
- 5-way joystick switch
- Laser-cut acrylic + cardboard (designed in AutoCAD)

---

## Team

Built by **Wanderlust Gaming Co.** — Presthika Vijaykumar, Ariba Khan, Jaydon Mac, Molly Herringshaw

Northeastern University · Cornerstone of Engineering I · Fall 2025
