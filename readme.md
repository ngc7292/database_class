# database lab big homework

## build

```shell
pip install -r requierment.txt

python manage.py migrate
python manage.py makemigrations

```


## api

date形式 xxxx-xx-xx iso时间格式

check_in
```
requests
{
	'name':'xxx',
	'id_number':'',
	'room_number':'',
	'date':'xxxx-xx-xx'
}
response
{
	'status':['seccuss'.'error'],
	'msg':'xxx'	
}
```

settle
结账分为2部分，首先查找未完成的账单，其次结账
可分为两个api
```
requests
{
	'name':'',
	'id_number':'xxxx'
}
response
{
	'id':'',
	'id_number':'',
	'name':'',
	'room_number':'',
	'date':'',
	'price':''
}
```

settle_finish
```
requests
['xx','xx']
response
{
	'status':'xxx',
	'msg':'xxxx'
}
```

group_book
```
requests
{
	'org_name':'xx',
	'member':[{
		'name':'',
		'id_number':'',
		'room_number':''
	}
	...],
	'date':''
}
response
{
	'status':['seccuss'.'error'],
	'msg':'xxx'	
}
```

group_settle
```
requests
{
	'org_name':'xx',
}
response
{
	'orders':[{
		'id':'xx',
		'id_number':'xxx',
		'name':'xxx',
		'room_number':'xx',
		'date':'xxx',
		'price':'xxx',
}
```

group_settle_finsih

```
requests
['xx','xx']
response
{
	'status':'xxx',
	'msg':'xxxx'
}
```

check_guest_info

```
requests
{
	'name':['xxx','xxx'],
	'id_number':['xxxx','xxxx'],
	'room_number:['xxx','xxxx']
}
response
{
	'guests_info':[{
		'name':'xxx',
		'id_number':'xxx',
		'is_live':'xxx',
		'last_live_room':'',
	}]
}
```

check_room

```
get

response
{
	'room_info':[{
		'room_number':'xxx',
		'room_type':'xxx',
		'is_live':'xxx',
		'is_book':'xxx',
		'room_price':'',
	}]
}
```

change_room 你自己想想吧，我不知道怎么写了