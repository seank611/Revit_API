# material_takeoff.py V1.0 5/8/2021
# Copyright of Sean Kelton
# pull revit output file and determine quantities, write to excel file
from pathlib import Path
import pandas as pd
import openpyxl as xl
from openpyxl.styles import Alignment, Font
from openpyxl import Workbook
from takeoffutils import list_check, mat_assign, df_toexcel

csv_file = r"C:\Users\seank\Documents\Python\Revit API\CSV and Excel\revit_out.csv"

# out_path is a temporary variable, delete and have this be user specified in final program
path = r"C:\Users\seank\Documents\Python\Revit API\CSV and Excel"

def takeoff(csv_file, folder, file_name, group_by):

    path = Path(folder)
    # file_name = f'Revit Summary.xlsx'
    out_path = f'{path}\{file_name}'

    material_list = ['Concrete', 'Masonry', 'CFMF', 'Wood', 'Steel']

    # read csv file & create initial dataframe
    df_revit_out = pd.read_csv(csv_file)

    # filter down dataframe, eliminate 'Existing' construction
    df_new_struct = df_revit_out[df_revit_out['Phase Created'] != 'Existing']
    df_existing_struct = df_revit_out[df_revit_out['Phase Created'] == 'Existing']
    # assign materials to entries that are currently unassigned
    df_revit_out = mat_assign((df_revit_out))
    df_new_struct = mat_assign(df_new_struct)

    # CONCRETE: calc concrete volume in cubic yards: total conc; footings; floors
    # remove non-concrete materials from list
    df_concrete = df_new_struct[df_new_struct['Structural Material'] == 'Concrete']
    df_conc_sum = df_concrete.groupby([group_by], as_index=False)["Volume"].sum()
    # convert volume to cubic yards
    df_conc_sum["Volume"] = df_conc_sum["Volume"] * 0.037037
    # add row to dataframe with sum of volume column
    df_conc_sum.loc[len(df_conc_sum.index)] = ['Total Volume', df_conc_sum['Volume'].sum()]
    df_conc_sum.insert(0, 'Material', 'Concrete')

    # STEEL: calculate total steel weight by family
    df_steel = df_new_struct[df_new_struct['Structural Material'] == 'Steel']
    df_steel_sum = df_steel.groupby([group_by], as_index=False)["Volume"].sum()
    # convert steel volume to weight in (lbs)
    df_steel_sum["Volume"] = df_steel_sum["Volume"] * 490
    # add row to dataframe with sum of volume column
    df_steel_sum.loc[len(df_steel_sum.index)] = ['Total Steel Weight', df_steel_sum['Volume'].sum()]
    df_steel_sum.insert(0, 'Material', 'Steel')

    df_summary = pd.concat([df_conc_sum, df_steel_sum])
    df_summary.rename(columns={'Volume': 'Volume, Wt (CuY, lbs)'}, inplace=True)

    # send info to excel
    # export revit out dataframe to excel sheet:
    df_revit_out.to_excel(out_path, sheet_name='Revit Output', index=False)
    # export summary dataframe to excel:
    # df_summary.to_excel(r"C:\Users\seank\Documents\Python\Revit API\CSV and Excel\revit_summary.xlsx",
    #                        sheet_name='Summary', index=False)
    df_toexcel(out_path, df_summary, 'Summary')
    df_toexcel(out_path, df_steel_sum, 'Steel')

    print(df_summary)
    print('Operation Compelte')
    return

