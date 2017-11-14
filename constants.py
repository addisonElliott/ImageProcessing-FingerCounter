# This file contains all the constants that will not be regularly changed upon runtime
import os
import numpy as np

# Name of the application, organization that created the application and current version of the application
applicationName = 'Finger Counter'
organizationName = 'Southern Illinois University Edwardsville'
version = '1.0.0'

# Directories for training and testing
trainingDir = os.path.join('data', 'training')
testingDir = os.path.join('data', 'testing')

# Angle in degrees that each convexity defect must be less than to be considered
# a valid finger webbing
fingerAngleThreshold = 95