#include <stdio.h>
#include <msgpack.h>

static msgpack_sbuffer* buffer = NULL;

void set_map_uint8_t(uint8_t* keystr, uint8_t value)
{
	sgpack_packer* pk = NULL;
        size_t off = 0;
        msgpack_unpacked key;
        msgpack_unpacked val;
        msgpack_unpack_return retkey;
        msgpack_unpack_return retval;
        msgpack_unpacked_init(&key);
        msgpack_unpacked_init(&val);

	if(buffer == NULL) {
		buffer = msgpack_sbuffer_new();
	}
	pk = msgpack_packer_new(buffer, msgpack_sbuffer_write);
	//msgpack_pack_map(pk, 1);
	msgpack_pack_str(pk, strlen(keystr));
	msgpack_pack_str_body(pk, key, strlen(keystr));
	msgpack_pack_uint8(pk, value);
	do {
		retkey = msgpack_unpack_next(&key, buffer->data, buffer->size, &off);
		retval = msgpack_unpack_next(&val, buffer->data, buffer->size, &off);
		if((key.data.type == MSGPACK_OBJECT_STR) && (strcmp(key.data.via.str.ptr, key) == 0)) {

		}
	} while (retkey == MSGPACK_UNPACK_SUCCESS);
}

int main(int argc, char** argv)
{
	int i = 0;
	uint8_t status_str[255];
	msgpack_sbuffer* buffer = msgpack_sbuffer_new();
	msgpack_packer* pk = msgpack_packer_new(buffer, msgpack_sbuffer_write);

//	msgpack_pack_map(pk, 2);

	memset(status_str, 0, 255);
	strcpy(status_str, "status.netdev");
	msgpack_pack_str(pk, strlen(status_str));
	msgpack_pack_str_body(pk, status_str, strlen(status_str));
	msgpack_pack_uint8(pk, 2);

	memset(status_str, 0, 255);
	strcpy(status_str, "status.mntbase");
	msgpack_pack_str(pk, strlen(status_str));
	msgpack_pack_str_body(pk, status_str, strlen(status_str));
	msgpack_pack_uint8(pk, 1);

	printf("%ld, %ld\n", buffer->size, buffer->alloc);
	for(i=0;i<buffer->size;i++) {
		printf("%x,", buffer->data[i]);
	}
	printf("\n");

//	msgpack_sbuffer_free(buffer);
	msgpack_packer_free(pk);

	pk = msgpack_packer_new(buffer, msgpack_sbuffer_write);

//	msgpack_pack_map(pk, 1);

	memset(status_str, 0, 255);
        strcpy(status_str, "status.netssh");
        msgpack_pack_str(pk, strlen(status_str));
        msgpack_pack_str_body(pk, status_str, strlen(status_str));
        msgpack_pack_uint8(pk, 2);

	memset(status_str, 0, 255);
	strcpy(status_str, "status.mntbase");
        msgpack_pack_str(pk, strlen(status_str));
	msgpack_pack_str_body(pk, status_str, strlen(status_str));
	msgpack_pack_uint8(pk, 2);

	printf("%ld, %ld\n", buffer->size, buffer->alloc);
	for(i=0;i<buffer->size;i++) {
		printf("%x,", buffer->data[i]);
	}
	printf("\n");

//	msgpack_sbuffer_free(buffer);
	msgpack_packer_free(pk);

	size_t off = 0;
	msgpack_unpacked key;
	msgpack_unpacked val;
	msgpack_unpack_return retkey;
	msgpack_unpack_return retval;
	msgpack_unpacked_init(&key);
	msgpack_unpacked_init(&val);
//	ret = msgpack_unpack_next(&key, buffer->data, buffer->size, &off);

	do {
		retkey = msgpack_unpack_next(&key, buffer->data, buffer->size, &off);
//		printf("key ret %x\n", retkey);
		retval = msgpack_unpack_next(&val, buffer->data, buffer->size, &off);
//		printf("val ret %x\n", retval);
		if((retkey != 0) && (retval != 0)) {
			printf("Key:");
			msgpack_object_print(stdout, key.data);
			printf(",");
			printf("Val:");
			msgpack_object_print(stdout, val.data);
			printf("\n");
		}
	} while (retkey == MSGPACK_UNPACK_SUCCESS);
	/*
	while (ret == MSGPACK_UNPACK_SUCCESS) {
		msgpack_object obj = result.data;
		msgpack_object_print(stdout, obj);
		printf("\n");
		ret = msgpack_unpack_next(&result, buffer->data, buffer->size, &off);
	}
	*/
	msgpack_unpacked_destroy(&key);
	msgpack_unpacked_destroy(&val);
	msgpack_sbuffer_free(buffer);

	return 0;
}
