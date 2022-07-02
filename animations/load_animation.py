import time
import sys
from rich.console import Console

console = Console()

def load_animation(load_str, load_time):
    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0
      
    # used to keep the track of
    # the duration of animation
    counttime = 0        
      
    # pointer for travelling the loading string
    i = 0                     
  
    while (counttime != load_time):
          
        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.05) 
                              
        # converting the string to list
        # as string is immutable
              
        # displaying the resultant string
        sys.stdout.write(f"\r" + load_str + " " + animation[anicount])
        sys.stdout.flush()
          
        anicount = (anicount + 1)% 4
        counttime = counttime + 1
    sys.stdout.write(f"\r" + load_str + " ✅")
    sys.stdout.write("\n")