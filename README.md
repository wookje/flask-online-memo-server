# Online Memo Server

If not specified, default `Content-Type` is `application/json`.  
Default method is `POST`

## Sign up

`/user/signup`

#### Body
key|value
---|---
name|String
password|String

## Sign in

`/user/signin`

#### Headers
key|value
---|---
name|String
password|String

## My memo list

`/memo/list`

#### Headers
key|value
---|---
name|String
password|String

## Write memo

`/memo/write`

#### Headers
key|value
---|---
name|String
password|String

#### Body
key|value
---|---
title|String
body|String

## Update memo

`/memo/update`

#### Headers
key|value
---|---
name|String
password|String

#### Body
key|value
---|---
memo_id|int
title|String
body|String