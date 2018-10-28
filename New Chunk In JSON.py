import ijson
import json
import pandas as pd

def extract_pcs(json_filename, inputs):
    '''
    Accept a set of postal codes we want to extract
    Return a geoJSON of only postal codes that were in the set
    '''
    with open(json_filename, 'rb') as input_file:
        #us_postal_codes.geojson follows the geojson standard, but seems to wrap postal codes in two additional keys: FeatureCollection and features. Hence, each postal code is contained in features.items
        generator = ijson.items(input_file, 'features.item')
        gas = True
        i = 0
        output = []
        while(gas):
            for item in generator:
                if int(item['properties']['geoid']) in inputs:
                    print('found one! i is ' + str(i))
                    print(item['properties']['zip5'] + ' / ' + item['properties']['geoid'])
                    #ijson parses coordinates and lat/longs as Decimal(). Need to convert these to floats now so that they make sense as strings later

                    #convert the lat/long
                    item['properties']['longitude'] = float(item['properties']['longitude'])
                    item['properties']['latitude'] = float(item['properties']['latitude'])
                    
                    output.append(item)
                    print('finished one! i is ' + str(i))
                    print('len(output) is ' + str(len(output)))
                    
                i += 1   
                #stop running if we found all targets
                if(len(output) == len(inputs)):
                    print('Found all targets')
                    output = {"type": "FeatureCollection", "features": output}
                    try:
                        with open('output.geojson', 'w') as file:
                            file.write(json.dumps(output))
                    except:
                        print('write error! returning object')
                        return output
                    gas = False
                    break
                if i % 100 == 0:
                    print('i is ' + str(i))
                if i >= 1000:
                    print('out of gas! writing file and exiting')
                    try:
                        output = {"type": "FeatureCollection", "features": output}
                        with open('output.geojson', 'w') as file:
                            file.write(json.dumps(output))
                    except:
                        print('write error! returning object')
                        return output
                    gas = False                    
                    break
            print('Reached end. Did not find all targets')
            try:
                output = {"type": "FeatureCollection", "features": output}
                with open('output.geojson', 'w') as file:
                    file.write(json.dumps(output))
            except:
                print('write error! returning object')
                return sublist

if __name__ == '__main__':
    inputs = pd.read_csv('boston.csv')
    #boston_zips = set(inputs.areaCode.tolist())
    #boston_zips = set([2129, 2446, 2123, 2135, 2445, 2215])
    #boston_zips = set([601, 602, 603])
    boston_zips = set([2481])
    #parse_json('us_postal_codes.geojson')
    test = boston = extract_pcs('us_postal_codes.geojson', boston_zips)
    #print(test)
