# user-specific setting
#source ~/.bashrc

# python is aliased to python3 on the user's OS. If not the case, python3 should be the right command.
python models.py -tripDataPath '../data/hubway_trips.csv' -stationDataPath '../data/hubway_stations.csv' -outputPath 'model.p'
