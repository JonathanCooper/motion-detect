import cv2
import time
import os
from functions import send_alert
import logging
import configuration

# begin config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
threshold = 50
gif_size = 20
frame_output = '{}/tmp/{}.jpg'.format(configuration.project_root)
gif_dir = '{}/www/img'.format(configuration.project_root)
gif_name = '{}.gif'
lock_file = '{}/run/lock'.format(configuration.project_root)
y1, y2, x1, x2 = 185, 230, 355, 400 # these are the corners of the rectangle
#   you will use for motion detection; in my case, the top-right corner
#   of my door
#
# end config

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    result = cv2.bitwise_and(d1, d2)
    (value, result) = cv2.threshold(result, threshold, 255, cv2.THRESH_BINARY)
    scalar = cv2.sumElems(result)
    return scalar

#cam = cv2.VideoCapture(0)
#f1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)[y1:y2, x1:x2]
#f2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)[y1:y2, x1:x2]
#f3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)[y1:y2, x1:x2]

found = False
while True:
    if os.path.isfile(lock_file):
        logging.debug('Found lock file, sleeping for 15s')
        try:
            cam.release()
        except NameError:
            pass
        time.sleep(15)
        continue
    try:
        f1 = f2
        f2 = f3
        f3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)[y1:y2, x1:x2]
    except:
        logging.debug('cam was released, starting new capture')
        cam = cv2.VideoCapture(0)
        f1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)[y1:y2, x1:x2]
        f2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)[y1:y2, x1:x2]
        f3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)[y1:y2, x1:x2]
    if diffImg(f1, f2, f3)[0]: 
        logging.debug('motion detected, capturing {} frames'.format(gif_size))
        from images2gif import writeGif
        from PIL import Image
        
        file_names = []
        for i in xrange(gif_size):
            logging.debug('capturing image {}'.format(i))
            frame = cv2.cvtColor(cam.read()[1], cv2.IMREAD_COLOR)
            out_file = frame_output.format(i)
            cv2.imwrite(out_file, frame, [cv2.IMWRITE_JPEG_QUALITY, 45])
            file_names.append(out_file)
            time.sleep(0.25)
        images = [Image.open(fn) for fn in file_names]
        size = (300, 300)
        logging.debug('making thumbnails')
        for im in images:
            im.thumbnail(size, Image.ANTIALIAS)
        now = int(time.time())
        gifoutfile = '{}/{}'.format(gif_dir, gif_name.format(now))
        logging.debug('writing gif file')
        writeGif(gifoutfile, images, duration=0.25)
        logging.debug('cleaning up')
        for used in file_names:
            os.remove(used)
        logging.debug('sending alert')
        send_alert('http://{}/img/{}'.format(
            configuration.web_app_host,
            gif_name.format(now))
            )
        found = True
        logging.debug('alert sent, releasing cam and deactivating')
        cam.release()
        open(lock_file, 'w').close()
        os.chown(lock_file, 81, 81)
        time.sleep(30)
    #else:
    #    logging.debug('no motion detected')
    #time.sleep()
    
if not found:
    print 'No motion detected'
