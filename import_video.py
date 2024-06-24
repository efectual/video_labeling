import cv2
import os
import argparse
from tqdm import tqdm

def import_video(input_video, output_folder, output_format):
    # create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # open video file
    cap = cv2.VideoCapture(input_video)

    # get video file name
    video_name = os.path.basename(input_video)
    video_name = os.path.splitext(video_name)[0]

    # get video file extension
    video_extension = os.path.splitext(input_video)[1]

    # get video file fps
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # get video file frame count
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # get video file frame width
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # get video file frame height
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # get video file codec
    codec = cv2.VideoWriter_fourcc(*'XVID')

    # create video writer object
    out = cv2.VideoWriter(output_folder + '/' + video_name + '_imported' + video_extension, codec, fps, (frame_width, frame_height))

    # read video file frame by frame
    with tqdm(total=frame_count) as pbar:
        frame_number = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                # save frame to output folder
                if output_format == 'jpg':
                    image_name = f"{video_name}_{frame_number}.jpg"
                    cv2.imwrite(os.path.join(output_folder, image_name), frame)
                elif output_format == 'png':
                    image_name = f"{video_name}_{frame_number}.png"
                    cv2.imwrite(os.path.join(output_folder, image_name), frame)
                else:
                    raise ValueError("Invalid output format. Only 'jpg' and 'png' are supported.")
                frame_number += 1
                pbar.update(1)
            else:
                break

    # release video file and video writer objects
    cap.release()
    out.release()

    # close all OpenCV windows
    cv2.destroyAllWindows()

    return

if __name__ == '__main__':
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Import a video file and save all its frames to a folder with the same name as the video file')
    parser.add_argument('-i', '--input', help='input video file', required=True)
    parser.add_argument('-o', '--output', help='output folder', required=True)
    parser.add_argument('-f', '--format', help='output format (jpg or png)', required=True)
    args = parser.parse_args()

    # call import_video function
    import_video(args.input, args.output, args.format)
    
    print('Video imported successfully!')
