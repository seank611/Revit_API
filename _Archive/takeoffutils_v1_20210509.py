# takeoffutils.py V1.0 05/09/2021
# utilities and other functions that will be used in the revit takeoff application
import pandas as pd
import openpyxl as xl
from openpyxl.styles import Alignment, Font

# checks each list to verify the strings within it contain certain keywords
# meant to comb through lists of Type names and assign to structural materials
# returns two new lists: one with values that contain specified keywords, one with values that dont
def list_check(keywords, clist, smode=None):

    # single mode to check single value against keywords
    if smode is True:
        has_value = False
        for word in keywords:
            if clist.find(word) != -1:
                has_value = True

        return has_value

    # standard mode to check list against keywords, runs as default
    else:
        y_list = []
        n_list = []
        for item in clist:
            has_conc = False
            for word in keywords:
                if item.find(word) != -1:
                    has_conc = True
            if has_conc == True:
                y_list.append(item)
            else:
                n_list.append(item)

        return y_list, n_list

def mat_assign(dataframe):
    # define keywords for each material as lists
    conc_keywords = ['Concrete', 'Slab', 'Conc', 'Mat', 'Footing']
    masonry_keywords = ['Brick', 'Masonry', 'Rubble', 'CMU']
    cfmf_keywords = ['Mtl Stud']
    wood_keywords = ['Wood', 'Plywood', 'Sheathing', 'PLYWOOD', 'SHEATHING', 'WOOD']
    steel_keywords = ['Steel', 'Metal Roof Deck']
    # define list of materials
    material_list = ['Concrete', 'Masonry', 'CFMF', 'Wood', 'Steel']
    # define dictionary linking each material name to its corresponding list
    material_dict = {
        'Concrete': conc_keywords,
        'Masonry': masonry_keywords,
        'CFMF': cfmf_keywords,
        'Wood': wood_keywords,
        'Steel': steel_keywords
    }

    for material in material_list:

        for i in range(dataframe.shape[0]):
            st_mat = dataframe.iloc[i, 2]
            type = dataframe.iloc[i, 6]
            fam = dataframe.iloc[i, 3]
            if st_mat == 'na':
                is_mat = list_check(material_dict.get(material), type, smode=True)
                if is_mat is True:
                    dataframe.iloc[i, 2] = material
                    # print('coolbeams')
            if material == 'CFMF':
                if fam == 'Light Gauge-Joists':
                    dataframe.iloc[i, 2] = 'CFMF'

    return dataframe

def df_toexcel(wb_path, dataframe, sheetname):

    wb = xl.load_workbook(wb_path)

    # create new sheet to store summary data
    n_sheet = wb.create_sheet(title=sheetname)
    headers = dataframe.columns.tolist()
    size = dataframe.shape

    c = 'a'
    for head in headers:
        n_sheet[f'{c}1'].value = head
        n_sheet[f'{c}1'].alignment = Alignment(horizontal="center")
        n_sheet[f'{c}1'].font = Font(bold=True, underline="single")
        c = chr(ord(c) + 1)
    # loop to fill up new sheet with DataFrame data, starts at cell 'a2'
    c = 'a'
    for col in range(size[1]):
        i = 2
        for row in range(size[0]):
            n_sheet[f'{c}{i}'].value = dataframe.iloc[row][col]
            n_sheet[f'{c}{i}'].alignment = Alignment(horizontal="center")
            n_sheet.column_dimensions[c].width = 25
            i +=1
        c = chr(ord(c) + 1)

    wb.save(wb_path)

    return
