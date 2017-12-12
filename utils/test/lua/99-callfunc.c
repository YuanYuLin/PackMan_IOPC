#include <stdio.h>
#include <stdlib.h>

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

void bail(lua_State *L, char *msg) {
	fprintf(stderr, "\nFATAL ERROR:\n %s: %s\n\n", msg, lua_tostring(L, -1));
	exit(1);
}

int main(int argc, char** argv)
{
	//create a Lua state variable
	const char *k, *v;
	const char *str;
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
	lua_pushstring(L, "A");
	lua_pushstring(L, "B");

	if(lua_pcall(L, 2, 1, 0) != 0)
		bail(L, "AAAA");

	str = lua_tostring(L, -1);
	printf("T:%s\n", str);
	/*--- tweaktable end ---*/

	//close the Lua state
	lua_close(L);

	return 0;
}

