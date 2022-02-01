# Customer API Endpoints

---

**GET CUSTOMER**

---

**URL** : `customer_manager/customer?customer_email=praveen@abc.com`

**Method** : `GET`

**Auth required** : YES

#### Request:

```?customer_email=praveen@abc.com```

#### Response:

**Code** : `200 OK`

```json
{
    "id": 1,
    "first_name": "praveen",
    "last_name": "nataraj",
    "email_address": "praveen@abc.com"
}
```

When customer doesn't exists:

```json
{
    "success": false,
    "msg": "Customer with email praveen123@abc.com does not exists!!!"
}
```

<br/>

---

**CREATE CUSTOMER**

---

**URL** : `customer_manager/customers`

**Method** : `POST`

**Auth required** : YES

#### Request:
```json
{
    "first_name": "john",
    "last_name": "mathew",
    "email_address": "john@abc.com"
}
```


#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "success": true,
    "msg": "Customer with email john@abc.com is created!!!"
}
```

<br/>

---

**UPDATE CUSTOMER**

---

**URL** : `customer_manager/customers`

**Method** : `PUT`

**Auth required** : YES

#### Request:
```json
{
    "first_name": "john",
    "last_name": "mathew",
    "email_address": "john@abc.com"
}
```


#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "success": true,
    "msg": "Customer already exists with this email john@abc.com and other values are updated!!!"
}
```

## Note:
1. For Create and Update customer **email_address** is required!!!