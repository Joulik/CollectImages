import cv2
from datetime import datetime
import time

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
        observ_period_sec = int(input("Observation period (sec)? "))
    except ValueError:
        print("Please use integer numbers only")
        observ_period_sec = 30
        print("Observation period set to 30 seconds")

    return observ_length, observ_period_sec

def start_end_times(observ_length,observ_period_sec):
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
    #end = end + observ_period_sec + 1
    end += 1
    return start, end

def take_snapshot(cap,curr_t,img_n):
    '''
    Function to get construct image and its filename
    arg:
    cap (): cv2 video capture
    curr_t (float); current time
    img_n (int): image number
    returns:
    filename (str): image filename
    img (): image file
    '''
    timeObj = time.localtime(curr_t)
    filename = time.strftime("%Y-%m-%d-%H%M%S", timeObj) + ".jpg"
    print("Image {}: {}".format(img_n,filename))
    ret, img = cap.read()
    return filename,img

def main():
    # Get observation length and observation period from user input
    observation_length, observation_period = get_user_params()

    # Define start and end times
    start_time, end_time = start_end_times(observation_length, observation_period)

    # Open video stream and get size
    capture_stream = cv2.VideoCapture(0) # use VideoCapture(1) for USB webcam 
    print("Size of Video Input Stream: {}".format(get_video_input_size(capture_stream)))

    # Initialization of variables
    old = 0
    img_nbr = 0
    current_time = time.time()
    print("Image capture starts in {} seconds".format(observation_period))

    # Main loop
    while current_time < end_time:
        
        new = int(current_time - start_time) % observation_period
        delta = abs(new - old)
        bool_snapshot = delta==observation_period-1 and new==0

        if bool_snapshot:
            img_nbr += 1
            image_filename, image = take_snapshot(capture_stream,current_time,img_nbr)
            cv2.imwrite(image_filename, image)

        old = new
        current_time = time.time()

    capture_stream.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()