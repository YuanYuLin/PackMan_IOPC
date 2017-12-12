#include <stdio.h>
#include <stdlib.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

static lua_State *L = NULL;

void bail(lua_State *L, char *msg) {
	fprintf(stderr, "\nFATAL ERROR:\n %s: %s\n\n", msg, lua_tostring(L, -1));
	exit(1);
}

void fs_init()
{
	L = luaL_newstate();
	luaL_openlibs(L);
}

void fs_destroy()
{
	lua_close(L);
	L = NULL;
}

int fs_get_string(unsigned char* map, unsigned char* key, unsigned char* val)
{
	unsigned char result = 0;
	if(luaL_loadfile(L, "/tmp/fs_ops.lua"))
	{
		bail(L, __FILE__);
	}

	printf("%d\n", __LINE__);
	if(lua_pcall(L, 0, 0, 0))
	{
		bail(L, __FILE__);
	}

	printf("%d\n", __LINE__);
	lua_getglobal(L, "get_value");
	if(lua_pcall(L, 0, 0, 0))
	{
		bail(L, __FILE__);
	}
	printf("%d\n", __LINE__);
	lua_pushstring(L, map);
	lua_pushstring(L, key);
	printf("%d\n", __LINE__);
	// 2 args(map, key), 1 result(val)
	if (lua_pcall(L, 2, 1, 0) != 0) 
	{
		bail(L, __FILE__);
	}

	printf("%d\n", __LINE__);
	/* retrieve result */
	if (!lua_isstring(L, -1))
		bail(L, "function `f' must return a number");
	printf("%d\n", __LINE__);
	*val = (unsigned char*)lua_tostring(L, -1);
	lua_pop(L, 1);  /* pop returned value */
	return result;
}

int fs_get_int8(unsigned char* map, unsigned char* key, unsigned char *val)
{
	unsigned char result = 0;
	lua_Number lua_val = 0;
	if(luaL_loadfile(L, "/tmp/fs_ops.lua"))
	{
		bail(L, __FILE__);
	}

	if(lua_pcall(L, 0, 0, 0))
	{
		bail(L, __FILE__);
	}

	lua_getglobal(L, "get_number");
	if(lua_pcall(L, 0, 0, 0))
	{
		bail(L, __FILE__);
	}
	lua_pushstring(L, map);
	lua_pushstring(L, key);
	// 2 args(map, key), 1 result(val)
	if (lua_pcall(L, 2, 1, 0) != 0) 
	{
		bail(L, __FILE__);
	}

	/* retrieve result */
	if (!lua_isnumber(L, -1))
		bail(L, "function `f' must return a number");
	lua_val = lua_tonumber(L, -1);
	*val = (unsigned char)lua_val;
	lua_pop(L, 1);  /* pop returned value */
	return result;
}

int fs_set_int8(unsigned char* map, unsigned char* key, unsigned char val)
{
	unsigned char result = 0;
	if(luaL_loadfile(L, "/tmp/fs_ops.lua"))
	{
		bail(L, __FILE__);
	}

	if(lua_pcall(L, 0, 0, 0))
	{
		bail(L, __FILE__);
	}

	lua_getglobal(L, "set_number");
	if(lua_pcall(L, 0, 0, 0))
	{
		bail(L, __FILE__);
	}
	lua_pushstring(L, map);
	lua_pushstring(L, key);
	lua_pushnumber(L, val);
	// 3 args(map, key, val), 1 result(val)
	if (lua_pcall(L, 3, 1, 0) != 0) 
	{
		bail(L, __FILE__);
	}
	/* retrieve result */
	if (!lua_isboolean(L, -1))
		bail(L, "function `f' must return a number");
	result = lua_toboolean(L, -1);
	lua_pop(L, 1);  /* pop returned value */

	return result;
}

int main(int argc, char** argv)
{
	int result = -1;
	unsigned char f1[128] = {0};
	fs_init();
	result = fs_get_string("test", "f1", &f1[0]);
	printf("%s-%d:%s\n", __func__, __LINE__, f1);
	/*
	fs_set_int8("test", "f1", 25);
	printf("%s-%d:%d\n", __func__, __LINE__, f1);
	result = fs_get_int8("test", "f1", &f1);
	printf("%s-%d:%d\n", __func__, __LINE__, f1);
	*/
	fs_destroy();
	return 0;
}
