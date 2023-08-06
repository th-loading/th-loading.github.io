---
title: CS:APP Proxy Lab记录
date: 2023-07-17 15:54:04 
tags: CS

---

# 前置知识

代理软件，用于接受并转发HTTP请求。借助socket数据结构转发文件 -> 并行处理请求 -> 设置cache返回最近获得的网页内容。

网络代理Proxy，隐藏真实的目的IP，核心在于网络层的包装，应用层一般有https加密，后包装发给代理服务器，代理服务器解包装再发给服务端。

透明代理：借助网关，将所有的流量重定向到代理器，设备不需要做出设置。

## I/O

### unix i/o 

所有设备模型化为文件，所有的输入、输出都视作文件的读写。

打开文件：获得描述符，对应打开文件。Shell 创建的进程有三个打开问价你，STDIN标准输入，STDOUT标准输出，STDERR标准错误，_FILENO为对应描述符。

文件位置：起始偏移量 seek 可改变

读写文件：越界会触发EOF end of file 的条件，用于检测，而不是文件结尾有的符号。

文件类型：普通文件 | 目录文件 | 套接字（跨网络）... 

```c
// flag 如何访问，如何写 
fd = open(char* f, int flags, mode_t mode);

// 返回-1 需要表明异常状态；正数则代表已读的字符数量
ssize_t read(int fd, void *buf, size_t n);
ssize_t write(int fd, const void* buf, size_t n);

// 可能需要反复读，已得到应用程序要求的数量，一般出现在需要外部输入的情况
// robust io 确保一定可以读完要求的字符数
// rio_readn rio_writen借助while循环不断读入字符
// 带缓冲区的read，在用户空间多设置一个buf (对用户透明的数据结构)

// readn
static ssize_t rio_read(rio_t *rp, char *usrbuf, size_t n) {
    int cnt;
 	
    // 一次性读buffer的size，对于频繁少量的请求，能减少系统调用的次数。
    while (rp->rio_cnt <= 0) {
        rp->rio_cnt = read(rp->rio_fd, rp->rio_buf,
                           sizeof(rp->rio_buf));
        if (rp->rio_cnt < 0) {
            if (errno != EINTR) /* Interrupted by sig handler return */
                return -1;
        }
        else if (rp->rio_cnt == 0) /* EOF */
            return 0;
        else
            rp->rio_bufptr = rp->rio_buf; /* Reset buffer ptr */
    }
    
    // 把buffer已有的部分分配给usrbuf (不需要系统调用) 
    cnt = n;
    if (rp->rio_cnt < n)
        cnt = rp->rio_cnt;
    memcpy(usrbuf, rp->rio_bufptr, cnt);
    rp->rio_bufptr += cnt;
    rp->rio_cnt -= cnt;
    return cnt;
}

```

```c
// meta data 元数据 struct stat
#include <sys/types.h>
#include <dirent.h>
DIR *opendir(const char *name);

// The opendir function takes a pathname and returns a pointer to a directory stream.
// A stream is an abstraction for an ordered list of items, in this case a list of directory entries

// owner id / group id  chmod - owern - group - other user 
// sudo 输入当前的密码 加入group sudo，能够默认以root作为命令的执行者，但密码是自己的密码。 sudo bash 等价于 su root

// unix kernel represent open file
// descriptor table one process one table fd 0 1 2 stdin stdout stderr 
// open file table (可以只存在于terminal，也可以是存在于disk的，指示此时的读的位置) shared by all process - vnode table (access size type 等实体信息) 多个表项指向同一个vnode即是sharing 

// 若同一个进程想要同时读多个位置，则有多个open file table，同一个vnode节点
// fork后fd指向相同的open file table 表项（refcnt++），只有refcnt为0，才会删去该表项。

// IO 重定向 newfd 指向与oldfd 相同的表项
int dup2(int oldfd, int newfd);

```

### standard i/o 

C standard library libc.so

```c
// fopen fclose fread fwrite fgets fputs fscanf fprintf 
// 同样存在buffer操作
// The standard I/O library models an open file as a stream. To the programmer, a stream is a pointer to a structure of type FILE.
// A stream of type FILE is an abstraction for a file descriptor and a stream buffer.


// 此时才将buffer输出到stdout
fflush(stdout);

// fscanf rio_readlineb 用于text文件而不是二进制文件
// 不能用于网络的IO 使用sprintf sscanf format string  
// standard-io 是全双工的，对于input后的output（如write之后的read），需要及时fflush（清空缓冲区）或重定向当前文件读写的位置。同理output后input，也需要重新定位。
```

## 网络

Nework Interface Cart (NIC) (Adapter) 网卡，一个IP对应一个MAC（Arp），连接网络层与传输层。多个IP可以对应同一个MAC，但一般一个网卡在传输层接入一个网络。

Socket 对应IP的一个端口（文件描述符），kernel需要根据网络请求的端口选择唤醒的应用程序。

```c
// 创建套接字，不涉及系统调用，声明数据结构并获取fd
#include <sys/types.h>
#include <sys/socket.h>

// Returns: nonnegative descriptor if OK, −1 on error
int socket(int domain, int type, int protocol);
clientfd = Socket(AF_INET, SOCK_STREAM, 0);

// socket的数据结构
int connect(int clientfd, const struct sockaddr *addr, socklen_t addrlen);

// 大端序存储，该数据结构唯一对应一个抽象的socket地址
struct sockaddr_in {
	uint16_t sin_family; /* Protocol family (always AF_INET) */
 	// 端口与ip地址
    uint16_t sin_port; 
    struct in_addr sin_addr; 
	// padding 对齐长度 4Byte + 8Byte + 4Byte = 16Byte
    unsigned char sin_zero[8]; 
};

// 当时缺乏一个void* 可以指向任意socket的指针，需要一个更泛用的数据结构。
// 16Byte 
// bind (sock, (struct sockaddr *) &name, sizeof (name))
// 接收sockaddr 实际视作 sockaddr_in (根据sa_family) 借助Cast的特性
struct sockaddr {
	uint16_t sa_family; /* Protocol family */
	char sa_data[14]; /* Address data */
};

// 将clientfd和server的socket关联，addrlen在ip中等于sizeof(sockaddr_in)
// 系统调用，直到出现错误或成功连接才会返回 Returns: 0 if OK, −1 on error
int connect(int clientfd, const struct sockaddr *addr, socklen_t addrlen);
// (x:y, addr.sin_addr:addr.sin_port) 对应的连接可以表示为端口间的连接

// server 将server的fd与server的socket相关联。
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);

// 默认sockfd是主动套接字，存在于连接客户端 active socket，借助listen转换为监听套接字 - backlog对应最多能处理的socket
int listen(int sockfd, int backlog);

// Returns: nonnegative connected descriptor if OK, −1 on error 
// 生成connfd用于与客户端的连接
int accept(int listenfd, struct sockaddr *addr, int *addrlen);

// 将字符串转换为套接字 （类似于索引的过程），同一个函数可以用于各种套接字的生成
// 为了多线程设计，更多的细节 返回result addrinfo的链表
// 基于这些得到的套接字，客户端会尝试去连接，服务端可以尝试去bind

int getaddrinfo(const char *host, const char *service, const struct addrinfo *hints, struct addrinfo **result);

void freeaddrinfo(struct addrinfo *result);

// sockaddr 转换为各个参数
int getnameinfo(const struct sockaddr *sa, socklen_t salen, char *host, size_t hostlen, char *service, size_t servlen, int flags);

// 打印域名对应的ip
int main(int argc, char **argv) {
    struct addrinfo *p, *listp, hints;
    char buf[MAXLINE];
    int rc, flags;
    if (argc != 2) {
        fprintf(stderr, "usage: %s <domain name>\n", argv[0]);
        exit(0);
    }

    /* Get a list of addrinfo records */
    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_INET;       /* IPv4 only */
    hints.ai_socktype = SOCK_STREAM; /* Connections only */
    
    // 封装了DNS查询的实现
    if ((rc = getaddrinfo(argv[1], NULL, &hints, &listp)) != 0) {
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(rc));
        exit(1);
    }

    /* Walk the list and display each IP address */
    flags = NI_NUMERICHOST; /* Display address string instead of domain name */
    for (p = listp; p; p = p->ai_next) {
        // buf接受信息
        Getnameinfo(p->ai_addr, p->ai_addrlen, buf, MAXLINE, NULL, 0, flags);
        printf("%s\n", buf);
    }

    /* Clean up */
    Freeaddrinfo(listp);
    exit(0);
}
```



## HTTP

借助HTTP协议交互，通过HTML语言显示内容，浏览器解析内容。

因此返回的内容content需要指明MIME类型。

任意返回的内容以文件作为基本单位。

URL：主机的域名IP + URI（对应服务器中的文件 + ? 后传递的参数）

最短的URI是 '/'，一般浏览器会自动填充 '/'，服务器则同时返回对应的网页。

```shell
telnet www.aol.com 80

# Client: request line
GET / HTTP/1.1  

# Client: required HTTP/1.1 header  
# 附加的头一般用于中间的代理服务器识别是否已有副本，可以直接返回
# 还可以指明能够接收的一些MIME种类
Host: www.aol.com
```

### 动态内容

将参数传到子进程。

```c
// systemd(1) 所有进程的源进程
// pstree -p

// CGI program 指符合CGI标准的可运行程序
// GET /cgi-bin/adder?15000&213 HTTP/1.1
// 服务器calls fork to create a child process and calls execve to run the /cgi-bin/adder the child process sets the CGI environment variable QUERY_STRING to 15000&213 可通过get_env函数调用得到
// 输出时：dup2 function to redirect standard output to the connected descriptor that is associated with the client.

if ((buf = getenv("QUERY_STRING")) != NULL) {
	p = strchr(buf, ’&’);
	*p = ’\0’;
	strcpy(arg1, buf);
	strcpy(arg2, p + 1);
	n1 = atoi(arg1);
	n2 = atoi(arg2);
}
/* Make the response body */
fflush(stdout);
```



### 安全性

网站需要先先向CA机构申领数字证书，CA机构对证书明文Hash后用私钥加密，得到的数字签名颁发到网站。

客户端发起http请求，提供支持的hash -> 服务端返回数字证书 （得到正确的服务端公钥）-> 浏览器用密钥R进行对称加密（运算量小），用服务器公钥加密R -> 服务端按对应的R加密返回网络内容

因此基于浏览器的https请求，只要证书没有问题，就可以确保报文的来源。

# 具体流程

```C
/* Recommended max cache and object sizes */
#define MAX_CACHE_SIZE 1049000
#define MAX_OBJECT_SIZE 102400

char BUF[MAX_CACHE_SIZE];
char TMP[MAX_OBJECT_SIZE];
int LRU[10];
int cnt = 0, clk = 0;
char REC[10][2500];
sem_t mutex_cnt, write_lock, mutex_tmp;

// ignore
void sigpipe_handler(int sig) {
    return;
}

void init_sem() {
    sem_init(&mutex_cnt, 0, 1);
    sem_init(&mutex_tmp, 0, 1);
    sem_init(&write_lock, 0, 1);
}

int read_cache(int fd, char *fn) {
    int sign = 0, id;
    P(&mutex_cnt);
    if (cnt == 0) 
        P(&write_lock);
    cnt++;
    V(&mutex_cnt);

    for (int i = 0; i < 10; i++) {
        if (LRU[i] != -1 && strcmp(fn, REC[i]) == 0) {
            Rio_writen(fd, &BUF[MAX_OBJECT_SIZE * i], MAX_OBJECT_SIZE);
            sign = 1;
            id = i;
            break;
        }
    } 

    P(&mutex_cnt);
    cnt--;
    if (sign) {
        LRU[id] = clk++;
    }
    if (cnt == 0) {
        V(&write_lock);
    }
    V(&mutex_cnt);
    
    return sign;
}

void write_cache(char *fn, char *buf) {
    P(&write_lock);
    int cid, cv = INT_MAX;
    for (int i = 0; i < 10; i++) {
        if (LRU[i] < cv) {
            cv = LRU[i];
            cid = i;
        }
    }
    LRU[cid] = clk++;
    strcpy(&BUF[cid * MAX_OBJECT_SIZE], buf);
    strcpy(REC[cid], fn);
    V(&write_lock);
}

// 2500 Byte 存储信息int 250 Byte
/* You won't lose style points for including this long line in your code */
static const char *user_agent_hdr = "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) Gecko/20120305 Firefox/10.0.3\r\n";

void parse_cmd(char *url, char *host, char *port, char *method, char *uri); 

void *exe_cmd(void *vargp) {
    Pthread_detach(pthread_self());
    int client_fd, server_fd, stat;
    client_fd = *((int*)vargp);
    Free(vargp);
    char buf[MAXLINE], host[MAXLINE], port[MAXLINE], method[MAXLINE], uri[MAXLINE], header[MAXLINE];
    char PAK[MAX_OBJECT_SIZE + 1], SIGN[MAXLINE];
    char version[MAXLINE] = "HTTP/1.0";
    rio_t rio_c, rio_s;

    Rio_readinitb(&rio_c, client_fd);
    if (!Rio_readlineb(&rio_c, buf, MAXLINE))  //line:netp:doit:readrequest
        return NULL;
    printf("%s", buf);
    parse_cmd(buf, host, port, method, uri);
    // printf("HOST: %s\nPORT: %s\nMETHOD: %s\nURI: %s\n", host, port, method, uri);
    sprintf(SIGN, "%s %s %s %s", host, port, method, uri);
    printf("%s\n", SIGN);

    int in_cache = read_cache(client_fd, SIGN);
    if (in_cache) {
        printf("IN!\n");
        Close(client_fd);
        return NULL;
    }
    // 打开server并发送头文件
    server_fd = Open_clientfd(host, port); 
    // printf("%d\n", server_fd);
    Rio_readinitb(&rio_s, server_fd);
    sprintf(header, "%s %s %s\r\n", method, uri, version);
    sprintf(header, "%sConnection: close\r\n", header);
    sprintf(header, "%sProxy-Connection: close\r\n", header);
    sprintf(header, "%s%s\r\n", header, user_agent_hdr);
    printf("%s", header);
    Rio_writen(server_fd, header, sizeof(header));
    // printf("%s", header);

    int count = 0, sign = 0;
    // ? 是否全部Cache
    while ((stat = Rio_readnb(&rio_s, PAK, sizeof(PAK))) > 0) {
        // printf("%s", buf);
        // strcat(content, buf);
        // Rio_writen(client_fd, buf, sizeof(buf));
        // 说明是可Cache的
        if (count == 0 && stat <= sizeof(PAK) - 1) {
            printf("GET!\n");
            sign = 1;
            write_cache(SIGN, PAK);
            printf("%s", PAK);
            Rio_writen(client_fd, PAK, stat);
        }
        else {
            printf("LARGE!\n");
            Rio_writen(client_fd, PAK, sizeof(PAK));
            count++;
        }
    }
    Close(client_fd);
    Close(server_fd);
    // printf("%s", content);
    // Rio_writen(client_fd, content, sizeof(content));
    // printf("%d\n", stat);
    return NULL;
}


int main(int argc, char**argv) {
    // printf("%s", user_agent_hdr);
    int listenfd, connfd;
    char hostname[MAXLINE], port[MAXLINE];
    socklen_t clientlen;
    struct sockaddr_storage clientaddr;
    pthread_t tid;
    init_sem();
    
    // 处理Signal
    Signal(SIGPIPE, sigpipe_handler);

    printf("start\n");
    /* Check command line args */
    if (argc != 2) {
	    fprintf(stderr, "usage: %s <port>\n", argv[0]);
	    exit(1);
    }

    listenfd = Open_listenfd(argv[1]);
    while (1) {
	    clientlen = sizeof(clientaddr);
        int *tr = (int*)malloc(sizeof(int));
	    connfd = Accept(listenfd, (SA *)&clientaddr, &clientlen); //line:netp:tiny:accept
        *tr = connfd;
        Getnameinfo((SA *) &clientaddr, clientlen, hostname, MAXLINE, 
                    port, MAXLINE, 0);
        printf("Accepted connection from (%s, %s)\n", hostname, port);
        pthread_create(&tid, NULL, exe_cmd, tr);
        // char buf[100] = "ret\n";
        // Rio_writen(connfd, buf, sizeof(buf));
        // exe_cmd(connfd);
	    // Close(connfd);                                            //line:netp:tiny:close
    }

    // 
    return 0;
}

void parse_cmd(char *url, char *host, char *port, char *method, char *uri) {
    char *ptr;

    // 得到method
    ptr = strchr(url, ' ');
    *ptr = '\0'; 
    strcpy(method, url);
    ptr++;
    while (*ptr == ' ') 
        ptr++;
    url = ptr;
    
    // 删除http://
    ptr = strstr(url, "http://");
    if (ptr != NULL) 
        url = ptr + 7;

    // 忽略version
    ptr = strchr(url, ' ');
    if (ptr != NULL) 
        *ptr = '\0';

    // 处理uri
    ptr = strchr(url, '/');
    if (ptr != NULL) {
        strcpy(uri, ptr);
        *ptr = '\0';
    }
    else {
        strcpy(uri, "/");
    }

    // port 
    ptr = strchr(url, ':');
    if (ptr == NULL) {
        strcpy(port, "80");
    }
    else {
        strcpy(port, ptr + 1);
        *ptr = '\0';
    }

    strcpy(host, url);
}

```

totalScore: 70/70
