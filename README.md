# Online Memo Server

If not specified, default `Content-Type` is `application/json`.  
Default method is `POST`

---

## Sign up

`/user/signup`

### Body
key|value
---|---
name|String
password|String

### Response

`201 Created`

---

## Sign in

`/user/signin`

### Headers
key|value
---|---
name|String
password|String

### Response

`204 No Content`

---

## My memo list

`/memo/list`

### Headers
key|value
---|---
name|String
password|String

### Response

`200 OK`

returns list of memo defined as below.

key|value
---|---
memo_id|int
created|String
updated|String
title|String
body|String

---

## Write memo

`/memo/write`

### Headers
key|value
---|---
name|String
password|String

### Body
key|value
---|---
title|String
body|String

### Response

`201 Created`

---

## Update memo

`/memo/update`

### Headers
key|value
---|---
name|String
password|String

### Body
key|value
---|---
memo_id|int
title|String
body|String

### Response

`200 OK`