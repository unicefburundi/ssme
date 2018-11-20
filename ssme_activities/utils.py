import ijson


def get_columns():
    return ["longitude",
            "latitude",
            "altitude",
            "nom_fosa",
            "type_fosa",
            "statutfosa",
            "code_fosa",
            "commune",
            "colline",
            "s_colline",
            "nom_ds",
            "code_ds",
            "province",
            "code_prov",
            "quartier",
            "cellule"
            ]


def extract_gps(files):
    good_columns = get_columns()

    data = []
    for fl in files:
        with open(fl, 'r') as f:
            objects = ijson.items(f, 'item')
            for row in objects:
                selected_row = []
                for item in good_columns:
                    selected_row.append(row.get(item, None))
                data.append(selected_row)
    return data


def add_zero(value):
    value = str(value)
    if len(value) % 2:
        value = "0" + value
    return value


def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}}
        feature['geometry']['coordinates'] = [row[lon], row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson
