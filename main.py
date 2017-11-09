import os

from algorithm import *

trainingDir = os.path.join('data', 'training')
testingDir = os.path.join('data', 'testing')


def main():
    print('ECE438 - Image Processing Project')
    print('Hand Finger Counter & Detector')

    print('\nSelect an option:\n'
          '\t1. Get training results\n'
          '\t2. Get testing results\n')

    line = input()
    option = int(line)

    if option == 1:
        runAlgorithm(trainingDir)
    elif option == 2:
        runAlgorithm(testingDir)
    else:
        print('Invalid option entered')


if __name__ == '__main__':
    main()
