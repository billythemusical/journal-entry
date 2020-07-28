from aiy.board import Board, Led
from aiy.leds import Leds, Color, Pattern
import subprocess

leds = Leds()

def main():
    print('Waiting for button press, then we journal! (Ctrl-C for exit).')
    with Board() as board:
        while True:
            leds.pattern = Pattern.breathe(500)
            leds.update(Leds.rgb_pattern(Color.YELLOW))
            board.button.wait_for_press()
            # board.button.wait_for_release()
            print('>>> launching journal')
            board.led.state = Led.OFF
            subprocess.run(['python3', 'text_to_speech.py'])
            break


if __name__ == '__main__':
    main()
