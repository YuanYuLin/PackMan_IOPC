print("Priming run.")

GT = {}

function tellme()
	io.write("This is coming from lua.tellme.\n")
end

function square(n)
	io.write("Within callfuncscript.lua fcn, arg=")
	io.write(tostring(n))
	n=n*n
	io.write(", squre=")
	io.write(tostring(n))
	print(".")
	return n
end

function tweaktable(tab_in)
	--local tab_out = {numfields=1}
	local tab_out = {}
	tab_out.numfields = 1
	tab_in.hello = "World"
	for k,v in pairs(tab_in) do
		tab_out.numfields = tab_out.numfields + 1
		tab_out[tostring(k)] = string.upper(tostring(v))
		io.write(k)
		print()
	end
	tab_out.numfields = tostring(tab_out.numfields)
	io.write("At bottom of callfuncscript.lua tweaktable(), numfields=")
	io.write(tab_out.numfields)
	print()
	return tab_out
end

function table_init()
	GT.test = "Test"
end

function get_val(obj, key_list, key_index)
	key = key_list[key_index]
	local keys = key_list

	if key_index >= table.maxn(key_list) then
		return obj[key]
	end
	return get_val(obj[key], keys, key_index + 1)
end

function get_value(key)
	local a = {}
	a.b = {}
	a.b.c = {}
	a.b.c.d="hello world"
	local key_array = {}
	for k in string.gmatch(key, "%a+") do
		table.insert(key_array, k)
	end
	key_array_len = table.maxn(key_array)
	print(get_val(a, key_array, 2))
	return a
end

