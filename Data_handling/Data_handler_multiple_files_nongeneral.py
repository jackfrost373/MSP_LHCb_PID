import pandas as pd # To be able to easily manipulate the data from the .root files.
import uproot # To be able to open .root files and turn their contents into dataframes.
import numpy as np # To be able to use linspace.

file_numbers = np.linspace(0, 99, 100) # Makes an array to access every folder in /home/Shared/lhc.data/ganga/20.
total_data_kaon_pion = pd.DataFrame() # Dataframe that will be filled up with the pions and kaons from all files.
for x in file_numbers: # Loops through all the files.
    number = '%.0f' % x # Makes the file number a string for the filename. Formatting done to ensure the string represents no decimals.
    file = uproot.open('/home/Shared/lhcbdata/ganga/20/'+number+'/output/davinci_MC_PID.root') # Opens one of the .root files.
    tree = file["PiTree/DecayTree"] # Accesses the tree of the root file.
    df = tree.pandas.df() # Turns the tree into a dataframe.
    
    tracking = df[['TrackP', 'TrackPt', 'TrackChi2PerDof', 'TrackLikelihood', 'TrackGhostProbability', 'TrackFitMatchChi2', 'TrackCloneDist', 'TrackFitVeloChi2', 'TrackFitVeloNDoF', 'TrackFitTChi2', 'TrackFitTNDoF']] # Desired tracking variables.
    RICH = df[['RichUsedAero', 'RichUsedR1Gas', 'RichUsedR2Gas', 'RichAboveMuThres', 'RichAboveKaThres', 'RichDLLe', 'RichDLLmu', 'RichDLLmu', 'RichDLLk', 'RichDLLp', 'RichDLLbt']] # Desired RICH variables.
    CALO = df[['EcalPIDe', 'EcalPIDmu', 'HcalPIDe', 'HcalPIDmu', 'PrsPIDe', 'InAccBrem', 'BremPIDe']] # Desired CALO variable.
    VELO = df[['VeloCharge']] # Desired VELO variable.
    ID = df[['pi_TRUEID']] # Particle IDs, known from simulation.
    data = pd.concat([tracking, RICH, CALO, VELO, ID], axis = 1) # Strings all variables and the particle IDs together into one dataframe.
    
    data_kaon_pion = data[(data.pi_TRUEID == -211) | (data.pi_TRUEID == 211) | (data.pi_TRUEID == -321) | (data.pi_TRUEID == 321)] # Filters the data to contain only pions, kaons and their antiparticles.
    # replace each value by what it should be
    data_kaon_pion = data_kaon_pion.replace(to_replace= 211, value= 1) # Pions get the ID 1.
    data_kaon_pion = data_kaon_pion.replace(to_replace= -211, value= 1) # Antipions get ID 1.
    data_kaon_pion = data_kaon_pion.replace(to_replace= 321, value= 0) # Kaons get ID 0.
    data_kaon_pion = data_kaon_pion.replace(to_replace= -321, value= 0) # Antikaons get ID 0.
    total_data_kaon_pion = pd.concat([total_data_kaon_pion, data_kaon_pion], axis = 0) # Links the data from one file to that of the files before it.
    print('File '+number+ ': done') # To see progress during the process.
total_data_kaon_pion_hdf5 = total_data_kaon_pion.to_hdf('/home/Shared/students/particle_data_chungus_kaon0_pion1.h5', key = 'kaon_pion', format = 'table')