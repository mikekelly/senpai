# SENPAI - SENtient Process AI

SENPAI is an AI system that thinks in code. Its thoughts are executed on
your computer; allowing it to interact with, and learn from, the world.

SENPAI is an "AGI" that continually (re)builds itself, learns by doing,
and gets more capable over time. It is given a very minimal set of
initial skills/tools to get going, and is then encouraged to develop
tools for itself as it encounters problems and thinks about how to solve
them.

![SENPAI](image.png)

## How to run

SENPAI runs in a container, so you need docker & docker-compose
installed on your system.

1. Copy `.env.template` to `.env` and set everything above the optional config
   params.

2. Run `./wakeup-senpai`

### Other useful tools

* `./cortex-shell` will load a command line repl where you can give
  senpai instructions
* `./bash-shell` will give you a bash shell in a container

## TODO
* When looking for an answer from a webpage, consider following relevant links
* Make memory more sophisticated
