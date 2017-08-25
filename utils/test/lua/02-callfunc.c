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
	lua_State *L;
	L = luaL_newstate();
	//load Lua libraries
	luaL_openlibs(L);
	//load but do NOT run the Lua script file
	if (luaL_loadfile(L, "02-callfuncscript.lua"))
		bail(L, "luaL_loadfile() failed");

	printf("In C, calling Lua\n");

	//run the loaded Lua script
	if(lua_pcall(L, 0, 0, 0))
		bail(L, "lua_pcall() failed");

	/*--- tellme begin ---*/
	lua_getglobal(L, "tellme");
	if(lua_pcall(L, 0, 0, 0))
		bail(L, "lua_pcall() failed");

	printf("Back in C again\n");
	/*--- tellme end ---*/

	/*--- square begin ---*/
	lua_getglobal(L, "square");
	lua_pushnumber(L, 6);
	if(lua_pcall(L, 1, 1, 0))
		bail(L, "lua_pcall() failed");

	printf("Back in C again\n");
	int mynumber = lua_tonumber(L, -1);
	printf("Return number=%d\n", mynumber);
	/*--- square end ---*/

	/*--- tweaktable begin ---*/
	lua_getglobal(L, "tweaktable");
	lua_newtable(L);

	lua_pushliteral(L, "fname");
	lua_pushliteral(L, "Margie");
	lua_settable(L, -3);

	lua_pushliteral(L, "lname");
	lua_pushliteral(L, "Martinez");
	lua_settable(L, -3);

	if(lua_pcall(L, 1, 1, 0))
		bail(L, "lua_pcall() failed");

	printf("Back in C again\n");

	lua_pushnil(L);
	while (lua_next(L, -2)) {
		v = lua_tostring(L, -1);
		lua_pop(L, 1);
		k = lua_tostring(L, -1);

		printf("k=%s, v=%s\n", k, v);
	}
	/*--- tweaktable end ---*/

	/*--- init test begin ---*/
	lua_getglobal(L, "table_init");

	if(lua_pcall(L, 0, 0, 0))
		bail(L, "lua_pcall() failed");

	printf("Back in C again\n");

	lua_getglobal(L, "get_value");
	lua_pushstring(L, "a.b.c.d");

	if(lua_pcall(L, 1, 1, 0))
		bail(L, "lua_pcall() failed");
	
	/*
	while(lua_next(L, -1)) {
		printf("%s\n", lua_typename(L, lua_type(L, -1)));
		lua_pop(L, 1);
	}
	*/
	/*--- init test end ---*/


	//close the Lua state
	lua_close(L);

	return 0;
}

