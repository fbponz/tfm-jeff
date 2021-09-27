def get_centroide(polygons,element):
  import json
  from shapely.geometry import shape, GeometryCollection, Point, Polygon
  from shapely import wkt
  data = json.loads(polygons[1:-1])
  poly = Polygon(data)
  return poly.centroid.xy[element][0]

def get_seccensal(latitude,longitude, seccensales):
  from shapely.geometry import shape, GeometryCollection, Point, Polygon
  from shapely import wkt
  import json
  seccensal = 0
  point1 = Point(longitude, latitude)
  for i in range(len(seccensales)):
      poly = Polygon(json.loads(seccensales["geometry_coordinates"][i][1:-1]))
      if poly.contains(point1) == True:
          seccensal = seccensales["properties_coddistsec"][i]
          break
  return seccensal

def get_coordinates_from_string(street_name, apikey):
  import requests
  import json
  URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+str(street_name)+".json?access_token="+apikey
  r = requests.get(url = URL)
  data = r.json()
  return data['features'][0]['geometry']['coordinates']

def request_isochrone(lati,long,time, apikey):
  from shapely.geometry import shape, GeometryCollection, Point, Polygon
  import requests
  import json
  import pandas as pd
  URL = "https://api.mapbox.com/isochrone/v1/mapbox/walking/"+str(long)+","+str(lati)+"?contours_meters="+str(time)+"&contours_colors=6706ce&access_token="+apikey
  r = requests.get(url = URL)
  data = r.json()
  df = pd.json_normalize(data['features'])
  return Polygon(df["geometry.coordinates"][0])

def get_sum_of_poi(row, poi_df,ine_df):
  import pandas as pd
  import shapely
  from shapely.geometry import shape, GeometryCollection, Point, Polygon
  from shapely import wkt
  total_poi = 0.0
  total_habitantes = 0.0
  secciones_censales_lista = []
  list_poi_json = []
  for _, r in poi_df.iterrows():
    point1 = Point(r['longitude'], r['latitude'])
    Poly = shapely.wkt.loads(row['isochrone_500m'])
    if Poly.contains(point1) == True:
      row[r['type']] = row[r['type']] + 1.0
      total_poi = total_poi + 1.0
      list_poi_json.append({"type": r['type'],"longitude": r['longitude'],"latitude": r['latitude']})
      if r['coddistsec'] not in secciones_censales_lista:
        secciones_censales_lista.append(r['coddistsec'])
        total_habitantes = total_habitantes + get_habitantes(r['coddistsec'],ine_df)

  row['seccensales_poi'] = secciones_censales_lista    
  row['total_poi'] = total_poi
  row['list_of_poi'] = list_poi_json
  row['habitantes_total'] = total_habitantes
  return row

def get_habitantes(Code, dataset_ine_valencia):
  import pandas as pd
  is_code = dataset_ine_valencia.loc[:, 'Code'] == Code
  df_code = dataset_ine_valencia.loc[is_code]
  if df_code.empty == False:
    value = df_code['habitantes'].values
  else:
    value = 0.0
  return float(value)

def get_attractivity(row):
  import math
  atractivity = (((row['total_poi'])/(row['num_secciones_isocrona']))-((row['lavanderias'])/(row['num_secciones_isocrona']))+((row['habitantes_total'])/(row['num_secciones_isocrona'])))
  return atractivity

def get_distance_two_locations(lat1, lon1, lat2, lon2):
  import math
  rad=math.pi/180
  dlat=lat2-lat1
  dlon=lon2-lon1
  R=6372.795477598
  a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
  distancia=2*R*math.asin(math.sqrt(a))
  return distancia

def HuffModel(row,Alpha,Beta,num_tienda,total_tiendas):
  operand_A = 0
  sum = 0
  for id_laundry in range(total_tiendas):
    name_laundry = "dist_lavanderia_"+str(id_laundry)
    name_attrac = "attr_lavanderia_"+str(id_laundry)
    if (num_tienda == id_laundry):
      operand_A +=(pow(row[name_attrac],Alpha)/pow(row[name_laundry],Beta))
    sum +=(pow(row[name_attrac],Alpha)/pow(row[name_laundry],Beta))
  huff_prob = (operand_A / sum)
  return huff_prob

def api_jeff(request):
  from google.cloud import bigquery
  import pandas as pd
  import shapely
  import json
  import requests
  import math
  from shapely.geometry import shape, GeometryCollection, Point, Polygon
  from shapely import wkt
  """Responds to any HTTP request.
  Args:
      request (flask.Request): HTTP request object.
  Returns:
      The response text or any set of values that can be turned into a
      Response object using
      `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
  """
  request_json = request.get_json()
  if request_json and 'street_name' in request_json:
    vAPIKEYmpbx = #{Clave de Mapbox API}
    project_id = '{TuProyecto}'
    bqclient = bigquery.Client(project=project_id)
    # Query Bigquery tables
    query_string = "SELECT * FROM `{TuProyecto}.{NombreBigQuery}.lavanderias`"
    query_job = bqclient.query(query_string)  # API request
    rows = query_job.result()
    vlc_laundry = rows.to_dataframe()    
    query_string = "SELECT * FROM `{TuProyecto}.{NombreBigQuery}.poi_tratado`"
    query_job = bqclient.query(query_string)  # API request
    rows = query_job.result()
    poi_tratados = rows.to_dataframe()
    query_string = "SELECT habitantes,Code FROM `{TuProyecto}.{NombreBigQuery}.data_ine_vlc`"
    query_job = bqclient.query(query_string)  # API request
    rows = query_job.result()
    dataset_ine_valencia = rows.to_dataframe()
    query_string = "SELECT properties_coddistsec,geometry_coordinates FROM `{TuProyecto}.{NombreBigQuery}.seccensales_geocsv`"
    query_job = bqclient.query(query_string)  # API request
    rows = query_job.result()
    seccensales_geojson = rows.to_dataframe()
    query_string = "SELECT * FROM `{TuProyecto}.{NombreBigQuery}.output_huff_template`"
    query_job = bqclient.query(query_string)  # API request
    rows = query_job.result()
    df_output_huff = rows.to_dataframe()
    #Create Dataframe used for calculate output
    street_name = request_json['street_name'] 

    coordinates = get_coordinates_from_string(street_name, vAPIKEYmpbx)
    laundry_seccensal = get_seccensal(coordinates[1], coordinates[0], seccensales_geojson)
    new_row = {'name': 'new', 'rating': 0, 'user_ratings_total': 0, 'latitude': coordinates[1], 'longitude': coordinates[0], 'type': 'lavanderias', 'coddistsec': laundry_seccensal, 'subtypes': 'laundry'}
    vlc_laundry = vlc_laundry.append(new_row, ignore_index=True)
    element = len(vlc_laundry)-1
    vlc_laundry["isochrone_500m"][element] = request_isochrone(vlc_laundry["latitude"][element], vlc_laundry["longitude"][element], 500, vAPIKEYmpbx)
    vlc_laundry["isochrone_500m"][element] = str(vlc_laundry["isochrone_500m"][element])
    for i in vlc_laundry.columns:
      if ((i != 'latitude') and (i != 'longitude') and (i != 'subtypes') and (i != 'type') and (i!= 'name') and (i != 'coddistsec') and (i !='isochrone_500m')):
        vlc_laundry[i][element]= 0
    vlc_laundry.loc[element] = get_sum_of_poi(vlc_laundry.loc[element], poi_tratados,dataset_ine_valencia)
    vlc_laundry['num_secciones_isocrona'][element] = len(vlc_laundry['seccensales_poi'][element])
    vlc_laundry["atractividad"][element] = get_attractivity(vlc_laundry.loc[element])
    vlc_laundry["atractividad_percent"] = vlc_laundry["atractividad"] / vlc_laundry["atractividad"].max()
    name_laundry = "dist_lavanderia_"+str(element)
    df_output_huff[name_laundry] = df_output_huff.apply(lambda row: get_distance_two_locations(vlc_laundry['latitude'][element],vlc_laundry['longitude'][element],row['centroid_lat'],row['centroid_lng']), axis=1)

    name_attrac = "attr_lavanderia_"+str(element)
    df_output_huff[name_attrac] = vlc_laundry['atractividad_percent'][element]

    df_output_huff["Huff_Prob"] = df_output_huff.apply(lambda row: HuffModel(row,1,2,len(vlc_laundry)-1,len(vlc_laundry)), axis=1)

    lavan_new = vlc_laundry.tail(1)
    lavan_new.drop(['int64_field_0', 'Unnamed__0','name','user_ratings_total','type','subtypes','atractividad'], axis=1, inplace=True)
    huff_output = df_output_huff[["properties_coddistsec","Huff_Prob"]]
    huff_output_json = huff_output.to_json(orient='index')
    lavan_new["Prob_Huff"] = huff_output_json
    lavan_new_json = lavan_new.to_json(orient='index')

    return lavan_new_json
  else:
    return f'404'
