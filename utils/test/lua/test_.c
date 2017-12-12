#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

void bail(lua_State *L, char *msg) {
	fprintf(stderr, "\nFATAL ERROR:\n %s: %s\n\n", msg, lua_tostring(L, -1));
	exit(1);
}

uint8_t get_data(uint8_t* key, uint8_t* val, uint32_t val_max_len)
{
	const int8_t* str;
	lua_State *L;
	L = luaL_newstate();
	//load Lua libraries
	luaL_openlibs(L);
	//load but do NOT run the Lua script file
	if (luaL_loadfile(L, "/tmp/test.lua"))
		bail(L, "luaL_loadfile() failed");

	printf("In C, calling Lua\n");

	//run the loaded Lua script
	if(lua_pcall(L, 0, 0, 0))
		bail(L, "lua_pcall() failed");

	/*--- tweaktable begin ---*/
	lua_getglobal(L, "test_str");
	lua_pushstring(L, key);

	if(lua_pcall(L, 1, 2, 0) != 0)
		bail(L, "pushstring() failed");

	str = lua_tostring(L, -1);
	printf("%d\n", strlen(str));
	strcpy(val, str);
	/*--- tweaktable end ---*/

	//close the Lua state
	lua_close(L);
	return 0;
}

uint8_t get_string(uint8_t* key, uint8_t* val, uint32_t val_max_len)
{
	const int8_t* str;
	int i = 0;
	int top = 0;
	lua_State *L;
	L = luaL_newstate();
	//load Lua libraries
	luaL_openlibs(L);
	//load but do NOT run the Lua script file
	if (luaL_loadfile(L, "/tmp/test.lua"))
		bail(L, "luaL_loadfile() failed");

	printf("In C, calling Lua\n");

	//run the loaded Lua script
	if(lua_pcall(L, 0, 0, 0))
		bail(L, "lua_pcall() failed");

	/*--- tweaktable begin ---*/
	lua_getglobal(L, "func_name");
	lua_pushstring(L, key);

	if(lua_pcall(L, 1, 1, 0) != 0)
		bail(L, "AAAA");

	top = lua_gettop(L);
	for (i = top; i >= 1; i--){
		printf("type:%s\n", lua_typename(L, lua_type(L, i)));
	}
	printf("tt:%d\n", top);
	for(i = 1; i <= top; i++){
		lua_pushnumber(L, i);
		lua_gettable(L, -2);

		printf("type:%s\n", lua_typename(L, lua_type(L,-1)));
		switch(lua_type(L, -1)) {
			case LUA_TSTRING:
				printf("%s\n", lua_tostring(L, -1));
				break;
			case LUA_TBOOLEAN:
				printf("%d\n", lua_toboolean(L, -1));
				break;
			case LUA_TNUMBER:
				printf("%x\n", lua_tointeger(L, -1));
				break;
		}

		lua_pop(L, 1);
	}
	/*--- tweaktable end ---*/

	//close the Lua state
	lua_close(L);
	return 0;
}

int main(int argc, char** argv)
{
	uint8_t str[128] = {0};
	get_string("test", &str[0], 128);
	//printf("ABCDDD - %s\n", str);
}
