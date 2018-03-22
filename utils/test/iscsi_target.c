#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
struct iscsi_bsh_t {
	uint8_t opcode;
	uint8_t op_spec_1[3];
	uint8_t ahs_len;
	uint8_t data_seg_len[3];
	uint8_t op_spec_2[8];
	uint32_t init_tag;
	uint8_t op_spec_3[29];
}

struct iscsi_pdu_t {
}

int main(int argc, char** argv)
{
	int sockfd = -1;
	int clifd = -1;
	char buf[1024];
	int rc = 0;
	int i = 0;
	sockfd = socket(AF_INET , SOCK_STREAM , 0);
	if (sockfd == -1){
		printf("Fail to create a socket.");
	}

	struct sockaddr_in serverInfo,clientInfo;
	int addrlen = sizeof(clientInfo);
	bzero(&serverInfo,sizeof(serverInfo));

	serverInfo.sin_family = PF_INET;
	serverInfo.sin_addr.s_addr = INADDR_ANY;
	serverInfo.sin_port = htons(3260);
	bind(sockfd,(struct sockaddr *)&serverInfo,sizeof(serverInfo));
	listen(sockfd,5);

	while(1){
		clifd = accept(sockfd,(struct sockaddr*) &clientInfo, &addrlen);
		//send(clifd,message,sizeof(message),0);
		rc = recv(clifd,buf,sizeof(buf),0);
		//printf("Get:%s\n",inputBuffer);
		printf("cfd:%x, \n", clifd);
		printf("rc:%d\n", rc);
		for(i=0;i<rc;i++) {
			if((i%16) == 0)
				printf("\n");
			printf("%02x,", buf[i]);
		}
	}
	return 0;
}
