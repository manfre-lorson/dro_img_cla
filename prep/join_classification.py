'''
after creating the tiles from the orig drone image
- creating a shapefile with "create fishnet"
    parameters:
        fishnet origin coordinat:
            x coordinate: 565291,6921100001     y coordinate: 4654531,021310001
            X coordinate: 565291,6921100001     y coordinate: 4654541,021310001

            cell size width : 14.545
            cell size height:-14.545
            number of rows: 341
            number of columns: 341

        create polygons


assign coordinate name to each created cell:

- create new field:
    as text
-field-calculator
    - python
    - show codeblock
        def pos(fid):
            x = fid%341
            y = fid/341
            return 'x{0}_y{1}'.format(x,y)

        pos(!FID!)


join

- join shapefile with classified shapefile from Carlos
    O:\Projects\Fieldwork\Peneda\NatureConservationCourse2017\Groups\Land_cover\WORK\LAND_COVER\land_cover_final_v2.shp
- spatial join
    - join data from another layer based on spatial location
    - sec option (each polygon will be given the attributes of the polygon if falls...)
- delete all not needed fields from the new shapefile

create csv with classes:

    data = mp.vector.shp_attr_tbl(r'S:\Florian_Wolf\Lab\drone_ki_slope\fishnet_tiles_classes.dbf')
    data.get_attr_tbl()
    df = data.attributes
    df = df.fillna('')
    df.to_csv(r'S:\Florian_Wolf\Lab\drone_ki_slope\tile_rgb_classes.csv')
'''
