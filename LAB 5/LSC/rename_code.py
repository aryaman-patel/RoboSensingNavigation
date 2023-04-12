import os
import glob


cwd = os.getcwd()
print(cwd)

# Get all the files in the current directory
files = glob.glob('*.jpg')


# Replace the file name with camera_calibration1.jpg, camera_calibration2.jpg, etc.
for i, file in enumerate(files):
    os.rename(file, 'LSC_' + str(i+1) + '.jpg')







