# Vehicle Data API Endpoints

---

**CREATE VEHICLE DATA**

---

**URL** : `vehicle_manager/vehicles`

**Method** : `POST`

**Auth required** : YES

#### Request:
```json
{
            "vin_number": "00Y47k8Z2N1FWeUMM",
            "tires":{"tires_0_name": "front-passenger"}
}
```


#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "data": {
        "license_plate": null,
        "id": 5,
        "vin_number": "00Y47k8Z2N1FWeUMM",
        "tires": {
            "tires_0_name": "front-passenger"
        },
        "battery_level": null,
        "fuel_level": null,
        "gps_position": null
    },
    "success": true
}
```

<br/>

---

**UPDATE VEHICLE DATA**

---

**URL** : `vehicle_manager/vehicles`

**Method** : `PUT`

**Auth required** : YES

#### Request:
```json
{
            "vin_number": "00Y47k8Z2N1FWeUMM",
            "tires":{"tires_0_name": "front-passenger", "tires_0_pressure": 49.0}
}
```


#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "data": {
        "license_plate": null,
        "id": 5,
        "vin_number": "00Y47k8Z2N1FWeUMM",
        "tires": {
            "tires_0_name": "front-passenger",
            "tires_0_pressure": 49.0
        },
        "battery_level": null,
        "fuel_level": null,
        "gps_position": null
    },
    "success": true
}
```

<br/>


---

**GET VEHICLE DATA**

---

**URL** : `vehicle_manager/vehicles/location?lat=139.121327&lon=-113.307143`

**Method** : `GET`

**Auth required** : YES

#### Request:
```vehicle_manager/vehicles/location?lat=139.121327&lon=-113.307143```

#### Response:

**Code** : `200 OK`

**Success**
When no vehicle data exists for the given location (latitude and longitude):
```json
{
    "data": [],
    "success": true
}
```
When data exists:
```json
{
    "data": [
        {
            "license_plate": "92qzBdT",
            "id": 1,
            "vin_number": "YDAxzg48nG3URCaAq",
            "tires": {
                "tires_0_name": "front-passenger",
                "tires_1_name": "front-driver",
                "tires_2_name": "rear-passenger",
                "tires_3_name": "rear-driver",
                "tires_0_pressure": 21.80286535515675,
                "tires_1_pressure": 39.2865661947938,
                "tires_2_pressure": 20.321588340530923,
                "tires_3_pressure": 17.281183636243885
            },
            "battery_level": 98,
            "fuel_level": 47,
            "gps_position": {
                "lat": -159.757973,
                "lng": 56.294881,
                "speed": 57.28401451531671,
                "updated_at": "2021-12-06T20:11:51.114Z"
            }
        }
    ],
    "success": true
}
```

<br/>

---

**DELETE VEHICLE DATA**

---

**URL** : `vehicle_manager/vehicles/{vin_number}`

**Method** : `DELETE`

**Auth required** : YES

#### Request:
```vin_number=00Y47k8Z2N1FWeUMM```

#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "success": true,
    "msg": "Records of vehicle with vin number: 00Y47k8Z2N1FWeUMM got deleted!!!"
}
```

<br/>

---

**ATTACH VEHICLE TO CUSTOMER**

---

**URL** : `vehicle_manager/vehicles/customer/{customer_id}`

**Method** : `PUT`

**Auth required** : YES

#### Request:
```customer_id=2```

```json
{
    "customer_email": "praveen@abc.com",
    "vin_numbers": ["00Y47k8Z2N1FWeUMM", "01iAjsdRfuNK6NfHT", "praavee"]
}
```


#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "success": true,
    "msg": "Could not found vehicles with vin number(s): ['praavee']. Rest are mapped to customer!!!"
}
```
Maps to the available vehicles return vin numbers of those that are not found back!!!





NOTE:
Vehicle Data Structure:
```
1. tires: {"tire_pos_name": "value", ...etc}
2. gps_position: {
  "lat": latitude,
  "lng": longitude,
  "speed": speed of the vehicle at the position,
  "updated_at": datetime with TZ
}
3. vin_number: "unique vehicle vin" !!required
4. license_plate: "vehicle plate number"
5. battery_level: "vehicle battery level"
6. fuel_level: "vehicle fuel level"
```

