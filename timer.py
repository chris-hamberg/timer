import argparse, datetime, time, sys, os

MUSIC_DIRECTORY = 'Audio'

class Timer:

    '''
    A Count Down Timer. Given a number of hours and minutes, an 
    alarm will sound exactly after that amount of time has passed.
    '''

    def __init__(self):
        self.options    = None
        self.seconds    = None
        self.alarm_time = None
        self.sound      = None
        self.parser     = argparse.ArgumentParser()
       
    def main(self):
        ''' Delegate Main Processes '''
        options = self.parse(sys.argv[1:]) # parse cmdline args

        try:
            self.seconds = self.total_seconds( # mins + hrs in seconds
                    options.minutes, options.hours)
        except ValueError as error:
            print(f'error: {error}')
            sys.exit(self.parser.print_help())
        self.schedule()          # the time the alarm will go off
        self.sound_picker()      # get an audio file
        self.wait()              # count down to alarm
        os.system(f'paplay {self.sound}')

    def parse(self, *args):
        ''' Basic cmdline parser '''
        self.parser.add_argument('-m', '--minutes', required=True, 
                action='store', choices=list(map(str, range(60)
                    )), metavar="[0-59]")
        self.parser.add_argument('-o', '--hours',
                action='store', choices=list(map(str, range(24)
                    )), metavar="[0-23]")
        return self.parser.parse_args(*args)

    def total_seconds(self, *args, hours=None, minutes=None, **kwargs):
        # TODO Seconds class
        ''' Covert hours to minutes. Sum total minutes.
        Convert sum to seconds. Seconds must be greater than 0.

            Fully decoupled method.

            *args over write all other args.

            Maximum of 2 *args and minimum of 1 *args are accepted.

            Assumes the first *arg is in minutes.

            Assumes *args is in minutes if only one *args is given

            If 2 *args are given then they are interpreted as [minutes, hours],
            and the rest of the args are ignored.

            **kwargs is provided as a fallback.
        '''
        def defaults():
            try:
                assert (minutes or hours)
            except AssertionError as fallback_kwargs:
                return False
            else:
                return True

        def keywords():
            try:
                assert kwargs
                minutes = kwargs.get('minutes', 0)
                hours = kwargs.get('hours', 0)
                return minutes, hours
            except AssertionError as fatal:
                raise ValueError('Function requires an integer argument.')

        try:
            # Validate *args or start falling back.
            assert 1 <= len(args) <= 2
            if len(args) is 2:
                minutes, hours = args
            else:
                minutes, hours = *args, hours
        except AssertionError as malformed_args:
            minutes, hours = keywords() if not defaults() else (minutes, hours)
        finally:
            # eliminate NoneTypes
            minutes, hours = minutes or 0, hours or 0

        try:
            inf = float('inf') # needed for comparison at the end.
            minutes, hours = map(float, (minutes, hours))
            minutes = sum([hours*60, minutes])
            seconds = minutes*60
            1/seconds # seconds is nonzero or ZeroDivisionError.
            assert (-1*inf < seconds < inf) # seconds is in real numbers.
        except ValueError as alphabetic:
            alphabetic.message = 'Input cannot be a letter.'
            raise
        except ZeroDivisionError as zero:
            raise ValueError('Calculated zero total seconds.')
        except AssertionError as overflow:
            raise OverflowError('Input cannot be infinity')
        else:
            return int(seconds)

    def schedule(self):
        ''' Finds the time the alarm will sound. As digital display. '''
        timezone   = datetime.timezone(datetime.timedelta(hours=-5), 'EST5ETD')
        now        = datetime.datetime.utcnow().astimezone(timezone)
        alarm_time = now + datetime.timedelta(seconds=self.seconds)
        self.alarm_time = alarm_time.strftime('%I:%M:%S %P')
        return self.alarm_time

    def wait(self):
        ''' Count Down the total # of secs before the alarm goes off. '''
        display = Display(self.sound, self.alarm_time, self.seconds)
        os.system('clear')
        print(display.header)
        for data in display.update():
            print(data, end='\r')
            time.sleep(1)
        else: print()

    def sound_picker(self):
        ''' Prompt user for audio file, and apply it to the alarm. '''
        sound = SoundPicker()
        sound.get()
        while not self.sound:
            os.system('clear')
            self.sound = sound.choose()

class Display:

    '''
    Displays the count down in seconds along with the time the alarm
    will sound.
    '''

    def __init__(self, sound, alarm_time, seconds):
        self._header    = None
        self.sound      = sound.split(os.sep)[-1]
        self.alarm_time = alarm_time
        self.seconds    = seconds
        self.col1       = ' alarm @'
        self.col2       = '\u2208'
        self.col3       = ' audio'
        self.space1     = self.margins(self.alarm_time, self.col1) +' '
        self.space2     = ' '*5
        self.space3     = self.margins(self.sound, self.col3)
        self.string()

    @property
    def header(self):
        return self._header

    def margins(self, data, pad):
        return ' '*(len(data) - len(pad))

    def string(self):
        self._header = (f'{self.col1}{self.space1} | '
                        f'{self.space2}{self.col2} | '
                        f'{self.space3}{self.col3}')
 
    def update(self):
        ''' Generates a new row for each second in the count down '''
        for second in range(self.seconds, 0, -1):
            yield f' {self.alarm_time} | {second: >5}s | {self.sound}'
 
class SoundPicker:

    '''
    Lets the user choose and alarm sound from MUSIC_DIRECTORY
    '''

    DIRECTORY = MUSIC_DIRECTORY

    def __init__(self):
        self.sounds    = dict()
        self.directory = os.path.join(os.environ['HOME'], SoundPicker.DIRECTORY)

    def get(self):
        ''' Gets file names from MUSIC_DIRECTORY and puts them in a dict. '''
        for num, media in enumerate(os.listdir(self.directory)):
            num += 1
            self.sounds[str(num)] = media

    def choose(self):
        '''
        Displays MUSIC_DIRECTORY contents and prompt for user selection. 
        
        Validates the input.
        '''
        
        try:
            for media in self.sounds.keys():
                print(f' {media: >2}. {self.sounds[media]}')
            sound = self.sounds[input(' select number > ')]
        except KeyError as invalid:
            input(' selection must be a number in the list... \n')
        else:
            return os.path.join(self.directory, sound)
 
if __name__ == '__main__':
    timer = Timer()
    timer.main()
