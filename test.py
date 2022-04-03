# just a test file to test out some code
import csv

# csv writer
# file name
file_path = r'C:\Users\seank\Desktop\seans.csv'
file_name = 'seans file.csv'
fields = ['Column 1', 'Column2', 'Another Column']

with open(file_path, 'w', newline='') as csvfile:
    # create writer object
    csvwriter = csv.writer(csvfile)
    # write headers
    csvwriter.writerow(fields)
    #create each row with for loop
    for r in range(5):
        row = [r, r*2, r-1, 'end']
        row.append(r*3)
        # append new row to csv file
        csvwriter.writerow(row)

words = ['8" (E) Rubble Fndn', 'Exterior - 10" Concrete', 'Exterior - 8" Concrete',
'8" Masonry Bearing Wall', '4" Mtl Stud Bearing Wall', '30" Mat Foundation',
'18" Mat Foundation', '8" Foundation Slab', '12" Foundation Slab', '(E) 3x10',
'3/4" PLYWOOD SHEATHING', 'D4- 2" LW Concrete on 9/16" Deck', 'D1- 3" LW Concrete on 1" Metal Deck',
'D3 1 1/2" Metal Roof Deck', '15"x19" Pier', '20"x14" Pier', '12"x19" Pier']

# for item in words:
#     print(item)
#     if item.find('Concrete') == -1:
#         print('not found')
#     else:
#         print('found')

keywords = ['Concrete', 'Slab', 'Mat', 'Footing']
y_list = []
n_list = []
for item in words:
    has_conc = False
    for word in keywords:
        if item.find(word) != -1:
            has_conc = True
    if has_conc == True:
        y_list.append(item)
    else:
        n_list.append(item)


if y_list.count('12"x19" Pier') != 0:
    print('value in list')
else:
    print('not found')

print(y_list)
print(n_list)

