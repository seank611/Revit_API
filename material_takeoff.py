# material_takeoff.py V1.2 10/05/2021
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

    df_conc_sum, df_conc_dtl = concrete_takeoff(df_new_struct, group_by)
    df_steel_sum, df_steel_dtl = steel_takeoff(df_new_struct, group_by)
    df_masonry_sum, df_masonry_dtl = masonry_takeoff(df_new_struct, group_by)
    df_wood_dtl = wood_takeoff(df_new_struct, group_by)
    df_cfmf_sum, df_cfmf_dtl = cfmf_takeoff(df_new_struct, group_by)

    df_summary = pd.concat([df_conc_sum, df_steel_sum, df_masonry_sum])
    df_summary.rename(columns={'Volume': 'Volume/Wt/Area (CuY/lbs/ft^2)'}, inplace=True)

    # Export into excel:
    # export revit out dataframe to excel sheet:
    df_revit_out.to_excel(out_path, sheet_name='Revit Output', index=False)
    # export summary dataframe to excel:
    # df_summary.to_excel(r"C:\Users\seank\Documents\Python\Revit API\CSV and Excel\revit_summary.xlsx",
    #                        sheet_name='Summary', index=False)
    df_toexcel(out_path, df_summary, 'Summary')
    df_toexcel(out_path, df_steel_dtl, 'Steel')
    df_toexcel(out_path, df_conc_dtl, 'Concrete')
    df_toexcel(out_path, df_masonry_dtl, 'Masonry')
    df_toexcel(out_path, df_wood_dtl, 'Wood')
    df_toexcel(out_path, df_cfmf_dtl, 'CFMF')

    print(df_summary)
    print('Operation Complete')
    return

def steel_takeoff(df_new_struct, group_by):
    # STEEL: calculate total steel weight by family
    df_steel = df_new_struct[df_new_struct['Structural Material'] == 'Steel']
    df_steel_sum = df_steel.groupby([group_by], as_index=False)["Volume"].sum()
    # convert steel volume to weight in (lbs)
    df_steel_sum["Volume"] = df_steel_sum["Volume"] * 490
    # add row to dataframe with sum of weight column
    df_steel_sum.loc[len(df_steel_sum.index)] = ['Total Steel Weight', df_steel_sum['Volume'].sum()]
    df_steel_sum.insert(0, 'Material', 'Steel')

    # Steel detail dataframe: quantities, weights, and lengths by member type
    df_steel_dtl = df_steel.groupby(['Type'], as_index=False)["Family"].count()
    df_temp = df_steel.groupby(['Type'], as_index=False)["Volume"].sum()
    df_steel_dtl['Total Weight (lbs)'] = df_temp["Volume"] * 490
    df_temp = df_steel.groupby(['Type'], as_index=False)["Length"].sum()
    df_steel_dtl['Net Length (ft)'] = df_temp["Length"]
    df_steel_dtl.rename(columns = {'Family': 'Quantity'}, inplace = True)

    return df_steel_sum, df_steel_dtl

def concrete_takeoff(df_new_struct, group_by):

    df_concrete = df_new_struct[df_new_struct['Structural Material'] == 'Concrete']
    df_conc_sum = df_concrete.groupby([group_by], as_index=False)["Volume"].sum()
    # convert volume to cubic yards
    df_conc_sum["Volume"] = df_conc_sum["Volume"] * 0.037037
    # add row to dataframe with sum of volume column
    df_conc_sum.loc[len(df_conc_sum.index)] = ['Total Volume', df_conc_sum['Volume'].sum()]
    df_conc_sum.insert(0, 'Material', 'Concrete')

    # Concrete detail dataframe: quantities, total volumes, and length by member type
    df_conc_dtl = df_concrete.groupby(['Type'], as_index=False)['Family'].count()
    df_temp = df_concrete.groupby(['Type'], as_index=False)["Volume"].sum()
    df_conc_dtl['Total Volume (CY)'] = df_temp["Volume"] * 0.037037
    df_temp = df_concrete.groupby(['Type'], as_index=False)["Length"].sum()
    df_conc_dtl['Total Length (ft)'] = df_temp["Length"]
    df_conc_dtl.rename(columns = {'Family': 'Quantity'}, inplace = True)

    return df_conc_sum, df_conc_dtl

def masonry_takeoff(df_new_struct, group_by):

    df_masonry = df_new_struct[df_new_struct['Structural Material'] == 'Masonry']
    # group by family for net masonry area
    df_masonry_sum = df_masonry.groupby([group_by], as_index=False)["Area"].sum()
    df_masonry_sum.rename(columns={'Area': 'Volume'}, inplace=True)

    # Masonry detail dataframe: sum of area's, grouped by type
    df_masonry_dtl = df_masonry.groupby(['Type'], as_index=False)['Family'].count()
    df_temp = df_masonry.groupby(['Type'], as_index=False)["Area"].sum()
    df_masonry_dtl['Total Area (ft^2)'] = df_temp["Area"]
    df_masonry_dtl.rename(columns={'Family': 'Quantity'}, inplace=True)
    df_masonry_sum.insert(0, 'Material', 'Masonry')

    return df_masonry_sum, df_masonry_dtl

def wood_takeoff(df_new_struct, group_by):

    df_wood = df_new_struct[df_new_struct['Structural Material'] == 'Wood']

    df_wood_dtl = df_wood.groupby(['Type'], as_index=False)['Family'].count()
    df_temp = df_wood.groupby(['Type'], as_index=False)['Area'].sum()
    df_wood_dtl['Total Area (ft^2)'] = df_temp['Area']
    df_temp = df_wood.groupby(['Type'], as_index=False)['Length'].sum()
    df_wood_dtl['Totel Length (ft)'] = df_temp['Length']

    df_wood_dtl.rename(columns={'Family': 'Quantity'}, inplace=True)

    return df_wood_dtl

def cfmf_takeoff(df_new_struct, group_by):

    df_cfmf = df_new_struct[df_new_struct['Structural Material'] == 'CFMF']
    df_cfmf_sum = df_cfmf.groupby([group_by], as_index=False)["Volume"].sum()
    # convert cfmf/steel volume to weight in (lbs)
    df_cfmf_sum["Volume"] = df_cfmf_sum["Volume"] * 490
    # add row to dataframe with sum of weight column
    df_cfmf_sum.loc[len(df_cfmf_sum.index)] = ['Total Steel Weight', df_cfmf_sum['Volume'].sum()]
    df_cfmf_sum.insert(0, 'Material', 'CFMF')

    # Steel detail dataframe: quantities, weights, and lengths by member type
    df_cfmf_dtl = df_cfmf.groupby(['Type'], as_index=False)["Family"].count()
    df_temp = df_cfmf.groupby(['Type'], as_index=False)["Volume"].sum()
    df_cfmf_dtl['Total Weight (lbs)'] = df_temp["Volume"] * 490
    df_temp = df_cfmf.groupby(['Type'], as_index=False)["Length"].sum()
    df_cfmf_dtl['Net Length (ft)'] = df_temp["Length"]
    df_cfmf_dtl.rename(columns = {'Family': 'Quantity'}, inplace = True)

    return df_cfmf_sum, df_cfmf_dtl
