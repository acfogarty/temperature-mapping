import pandas as pd
from pathlib import Path

def main():
    file_rec="records.csv"
    df_rec = read_records_file(file_rec)
    
    results_dict = dict()
    for location in get_locations_array(df_rec):
        df_loc = get_all_data_for_location(location, df_rec)
        write_result(location, df_loc)
        results_dict[location] = df_loc 

def read_records_file(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)
        
def read_excel(file: str) -> pd.DataFrame:
    return pd.read_excel(file, sheet_name='List', skiprows=28)

def write_result(loc: str, df: pd.DataFrame):
    fileout_name = str(loc+'.csv')
    fileout = Path('results/'+fileout_name)  
    fileout.parent.mkdir(parents=True, exist_ok=True)
    df[['Time','Temperature°C']].to_csv(fileout,index=False)

def get_locations_array(df: pd.DataFrame) -> list:
    return df['location'].unique()

def get_location_data(file: str) -> pd.DataFrame:
    df = read_excel(file)
    df = df[['No.','Time','Temperature°C']]
    df['Time']=pd.to_datetime(df['Time'],format='%d-%m-%Y %H:%M:%S')
    return df

def get_all_data_for_location(loc: str, df_rec: pd.DataFrame) -> pd.DataFrame:
    mask = df_rec['location']==loc
    files_list = df_rec[mask]['file_name']
    df_loc = pd.DataFrame()

    for file in files_list:
        print('Treating ',loc,file)
        df_aux = get_location_data('data/'+file)
        df_loc = pd.concat([df_loc,df_aux])
    return df_loc.sort_values(by='Time')

if __name__ == '__main__':
    main()