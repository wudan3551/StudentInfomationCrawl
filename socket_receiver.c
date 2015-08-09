#include<stdio.h>
#include<string.h>    //strlen strcat
#include<stdlib.h>    //strlen
#include<sys/socket.h>
#include<arpa/inet.h> //inet_addr
#include<unistd.h>    //write
 
#include<pthread.h> //for threading , link with lpthread

#include <mysql/my_global.h>
#include <mysql/mysql.h>
 
void *connection_handler(void *);
void restore_data(char *);//user defined function
 
int main(int argc , char *argv[])
{
    int socket_desc , new_socket , c , *new_sock;
    struct sockaddr_in server , client;
    char *message;
     
    //Create socket 
	//socket_desc refers to "socket descriptor"
    socket_desc = socket(AF_INET , SOCK_STREAM , 0);//parameter:ipv4 protocol,full-duplex stream socket,TCP protocol
    if (socket_desc == -1)
    {
        printf("Could not create socket");
    }
     
    //Prepare the sockaddr_in structure
    server.sin_family = AF_INET;//ipv4 protocol
    server.sin_addr.s_addr = inet_addr("121.43.109.2");//ip address(now this address is the address of my server )
    server.sin_port = htons(9988);//port number
     
    //Bind
    if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
    {
        puts("bind failed");
        return 1;
    }
    puts("bind done");
     
    //Listen
    listen(socket_desc , 3);//parameter:socket descriptor,maximum link number
     
    //Accept and incoming connection
    puts("Waiting for incoming connections...");
    c = sizeof(struct sockaddr_in);
	//once accept a socket connection,system will reallocate a socket descriptor -- new_socket
	//the following statement using "=" but not "==",so this is a infinity loop
    while( (new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c)) )
    {
        puts("Connection accepted");
         
        //Reply to the client
        message = "Hello Client , I have received your connection. And now I will assign a handler for you\n";
        write(new_socket , message , strlen(message));
         
        pthread_t sniffer_thread;//a unsigned int number,which used as thread identifier
        new_sock = malloc(1);
        *new_sock = new_socket;
         
        if( pthread_create( &sniffer_thread , NULL ,  connection_handler , (void*) new_sock) < 0)
        {
            perror("could not create thread");
            return 1;
        }
         
        //Now join the thread , so that we dont terminate before the thread
        //pthread_join( sniffer_thread , NULL);
        puts("Handler assigned");
    }
     
    if (new_socket<0)
    {
        perror("accept failed");
        return 1;
    }
     
    return 0;
}
 
/*
	prototype function to be executed by  the thread,
 	This will handle connection for each client.
*/
void *connection_handler(void *socket_desc)
{
    //Get the socket descriptor
    int sock = *(int*)socket_desc;
    int read_size;
    char *message , client_message[2000];
    
    message = (char *) malloc(256); 
    //Send some messages to the client
    message = "Greetings! I am your connection handler\n";
    write(sock , message , strlen(message));
     
    message = "Now type something and i shall repeat what you type \n";
    write(sock , message , strlen(message));
     
    //Receive a message from client
    while( (read_size = recv(sock , client_message , 2000 , 0)) > 0 )
    {
        //Send back the message back to client
        //write(sock , client_message , strlen(client_message));
		if(strlen(client_message) == 11){
			restore_data(client_message);
			printf("Received String:%s \n",client_message);
			*(client_message) = '\0';
		}
    }
     
    if(read_size == 0)
    {
        puts("Client disconnected");
        fflush(stdout);
    }
    else if(read_size == -1)
    {
        perror("recv failed");
    }
         
    //Free the socket pointer
    free(socket_desc);
    free(message); 
    return 0;
}
void restore_data(char *rec_data_package){ 

	MYSQL *conn;
  	my_ulonglong affected_rows;
  	//char rec_data_package[12] = {0x01,0x03,0x64,0x03,0x10,0x14,0x12,0x16,0x21,0x42,0x50,0x00};
	char user_id[10] = "";	
	char current[10] = "";
	char voltage[10] = "";
	char date[40] = "";
  	char *query_statement_seg1 = "INSERT INTO GPRS_TEST (user_id,current_leak,voltage,rec_time) VALUES(";
	char query_statement[500] = "";
	int current_value,voltage_value;

	current_value = (int)rec_data_package[1]*256 + (int)rec_data_package[2];
	voltage_value = (int)rec_data_package[3]*256 + (int)rec_data_package[4];
	
	//printf("current value is :%d\n",current_value);
	//*query_statement = "INSERT INTO GPRS_TEST (user_id,current_leak,voltage,rec_time) VALUES('0000','0.000','0.000','2000-01-01-00:00:00')";
    //int shift = 70;
	strcat(query_statement,query_statement_seg1);
	
	user_id[0] = 0x27;//single quote
	user_id[1] = 0x30 + *(rec_data_package)/1000;
	user_id[2] = 0x30 + (*(rec_data_package)%1000)/100;
	user_id[3] = 0x30 + (*(rec_data_package)%100)/10;
	user_id[4] = 0x30 + *(rec_data_package)%10;
	user_id[5] = 0x27;//single quote
	user_id[6] = 0x2C;//comma
	user_id[7] = 0x00;//end of string

	current[0] = 0x27;//single quote
	current[1] = 0x30 + (char)(current_value/1000);
	current[2] = 0x2E;//dot
	current[3] = 0x30 + (char)((current_value%1000)/100);
	current[4] = 0x30 + (char)((current_value%100)/10);
	current[5] = 0x30 + (char)(current_value%10);
	current[6] = 0x27;//single quote
	current[7] = 0x2C;//comma
	current[8] = 0x00;//end of string

	voltage[0] = 0x27;//single quote
	voltage[1] = 0x30 + (char)(voltage_value/1000);
	voltage[2] = 0x2E;//dot
	voltage[3] = 0x30 + (char)((voltage_value%1000)/100);
	voltage[4] = 0x30 + (char)((voltage_value%100)/10);
	voltage[5] = 0x30 + (char)(voltage_value%10);
	voltage[6] = 0x27;//single quote
	voltage[7] = 0x2C;//comma
	voltage[8] = 0x00;//end of string

	date[0] = 0x27;//single quote
	date[1] = 0x32;//2
	date[2] = 0x30;//0
	date[3] = 0x30 + (rec_data_package[5]>>4);
	date[4] = 0x30 + (rec_data_package[5]&0x0F);
	date[5] = 0x2D;//hyphen
	date[6] = 0x30 + (rec_data_package[6]>>4);
	date[7] = 0x30 + (rec_data_package[6]&0x0F);
	date[8] = 0x2D;//hyphen
	date[9] = 0x30 + (rec_data_package[7]>>4);
	date[10] = 0x30 + (rec_data_package[7]&0x0F);
	date[11] = 0x2D;//hyphen
	date[12] = 0x30 + (rec_data_package[8]>>4);
	date[13] = 0x30 + (rec_data_package[8]&0x0F);
	date[14] = 0x3A;//colon
	date[15] = 0x30 + (rec_data_package[9]>>4);
	date[16] = 0x30 + (rec_data_package[9]&0x0F);
	date[17] = 0x3A;//colon
	date[18] = 0x30 + (rec_data_package[10]>>4);
	date[19] = 0x30 + (rec_data_package[10]&0x0F);
	date[20] = 0x27;//single quote
	date[21] = 0x29;//close parethesis
	date[22] = 0x00;


	strcat(query_statement,user_id);
	
	strcat(query_statement,current);

	strcat(query_statement,voltage);

	strcat(query_statement,date);

	//printf("%s\n",rec_data_package);
	//printf("%s\n",query_statement);

	/* DataBase link initialization */
	conn = mysql_init(NULL);
  	/* Connect DataBase */
  	mysql_real_connect(conn, "localhost", "root", "abc6838338", "test", 0, NULL, 0);
	
	mysql_query(conn,query_statement);
  	
	affected_rows = mysql_affected_rows(conn);

  	printf("Affected Row is:%ld\n",(long)affected_rows);

  	if(affected_rows < 0)printf("Insert action failed!\n");

  	mysql_close(conn);//close mysql connection
	
	//return 0;
}
