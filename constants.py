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

# Size of patches
patchesSize = 25

# Percentage of tolerance for each patch to allow colors
# patchTolerance = np.array([0.2, 0.5, 0.8])
patchTolerance = np.array([0.2, 0.2, 0.2])