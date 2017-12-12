local t_cfg={
	['test']={
		['f1']=2,
	},
}

function get_number(map, key)
t_map = t_cfg[map]
val = t_map[key]
return val
end

function set_number(map, key, val)
t_map = t_cfg[map]
t_map[key]=val
return true
end

function main()
ret = get_number('test', 'f1')
print(ret) 
set_number('test', 'f1', 22)
ret = get_number('test', 'f1')
print(ret)
end

--main()
