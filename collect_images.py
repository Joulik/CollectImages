import cv2
import time
import winsound

def get_video_input_size(capture_stream):
    '''
    Function to obtain dimension of webcam image
    args:
    capture_stream (): Video capture from cv2
    returns:
    frame.shape (tuple): shape of webcam frame
    '''
    # Get frame from webcam
    _, frame = capture_stream.read()
    return frame.shape

def get_user_params():
    '''
    Function to obtain observation length and observation period from user
    returns:
    observ_length (int): total length of observation in minutes
    observ_period_sec (int): time between two snapshots in seconds
    filename_tag (str): tag for filename
    switch_period (int): time bewteen two A-B switches   
    '''
    # Get observation length
    try:
        observ_length = int(input("Observation length (min)? "))
    except ValueError:
        print("Please use integer numbers only")
        observ_length = 1
        print("Observation length set to 1 minute")

    # Get observation period i.e. time bewteen two snapshots
    try:
        observ_period_sec = int(input("Time period between two snapshots (sec)? "))
    except ValueError:
        print("Please use integer numbers only")
        observ_period_sec = 30
        print("Observation period set to 30 seconds")

    # Get tag for filename
    filename_tag = input("Tag for filename (str)? ")

    # Get AB-switch period
    try:
        switch_period = int(input("Switch period (sec)? [0 = no switching | should be a multiple of time period between two snapshots] "))
    except ValueError:
        print("Please use integer numbers only")
        switch_period = observ_period_sec / 2
        print("Switch period set to {}".format(switch_period))

    return observ_length, observ_period_sec, filename_tag, switch_period

def start_end_times(observ_length):
    '''
    Function to obtain observation start and end times
    args:
    observ_length (int): observation length in minutes 
    returns:
    start (float): start time of observation
    end (float): en time of observation 
    '''
    start = time.time()
    end = start + float(observ_length * 60)
    end += 1
    return start, end

def take_snapshot(cap, curr_t, img_n, fn_tg, AB_tg):
    '''
    Function to get construct image and its filename
    arg:
    cap (): cv2 video capture
    curr_t (float); current time
    img_n (int): image number
    fn_tg (str): filename tag
    AB_tag (str): A or B sequence
    returns:
    filename (str): image filename
    img (): image file
    '''
    timeObj = time.localtime(curr_t)
    filename = time.strftime(fn_tg + "_" + "%Y-%m-%d-%H%M%S" + AB_tg + ".jpg", timeObj)
    print("Image {}: {}".format(img_n, filename))

    ret, img = cap.read()
    return filename,img

def main():
    # Get observation length and observation period,
    # filename tag and switch period from user input
    observation_length, observation_period, filename_tag, switch_period = get_user_params()

    # Define start and end times
    start_time, end_time = start_end_times(observation_length)

    # Open video stream and get its shape
    capture_stream = cv2.VideoCapture(0) # use VideoCapture(1) for USB webcam 
    print("Size of Video Input Stream: {}".format(get_video_input_size(capture_stream)))

    # Beep parameters
    beep_freq = 880
    beep_duration = 250

    # Initialization of variables
    if switch_period != 0:
        AB_tag = "_A"
    else:
        AB_tag = ""
    old = 0
    old_switch = 0
    img_nbr = 0

    # Start
    current_time = time.time()
    print("Image capture starts in {} seconds".format(observation_period))

    # Main loop
    while current_time < end_time:
        
        # condition to trigger snapshot
        new = int(current_time - start_time) % observation_period
        delta = abs(new - old)
        bool_snapshot = delta==observation_period-1 and new==0

        # condition to trigger switch between A and B
        if switch_period !=0:
            new_switch = int(current_time - start_time) % switch_period
            delta_switch = abs(new_switch - old_switch)
            bool_switch = delta_switch==switch_period-1 and new_switch==0
        else:
            bool_switch = False
            new_switch = 0

        # trigger snapshot
        if bool_snapshot:
            img_nbr += 1
            image_filename, image = take_snapshot(capture_stream, current_time, img_nbr, filename_tag, AB_tag)
            cv2.imwrite(image_filename, image)
        old = new

        # trigger switch between A and B
        if bool_switch:
            winsound.Beep(beep_freq, beep_duration)
            if AB_tag == "_A":
                AB_tag = "_B"
            elif AB_tag == "_B":
                AB_tag = "_A"
        old_switch = new_switch

        current_time = time.time()

    # Stop capture
    capture_stream.release()
    cv2.destroyAllWindows()

    # Beep to signal end
    winsound.Beep(1320,1000)

if __name__ == '__main__':
    main()