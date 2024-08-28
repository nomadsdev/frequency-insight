import keyboard as kb
from recording import Recorder as Rec

def main():
    rec = Rec()

    print("Press '1' to start recording, '0' to stop recording, 'q' to quit.")

    while True:
        event = kb.read_event()
        if event.event_type == kb.KEY_DOWN:
            if event.name == '1':
                rec.begin_recording()
                kb.wait('0')
                rec.end_recording()
            elif event.name == 'q':
                break

    rec.clean_up()

if __name__ == "__main__":
    main()