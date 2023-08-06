---
title: CS:APP Shell Lab记录
date: 2023-07-05 15:09:23 
tags: CS
---



# 前置知识

## 系统调用

C提供了异常处理，比提供了全局变量 errno（int），作为错误类型。

注意main函数中 if (pid == 0) { xxx } 的部分是子进程运行的代码。而main中剩余部分与Handler都属于父进程，其中包括所有对jobs的维护操作。

每次执行系统调用结束，从内核态转换态，包括进程结束等过程，每次Switch到当前进程时，都会检查一下signal，同时调用对应的handler。

使用sig_set作为signal的数据结构，而不是是队列，因此并不知道有多少子进程发送了信号，handler一般要借助while函数处理。

```c
if ((pid = fork()) < 0) {
	fprintf(stderr, "fork error: %s\n", strerror(errno));
	exit(0);
}
```

```c
#include <sys/types.h>
#include <unistd.h>

# 获得pid号
pid_t getpid(void);
pid_t getppid(void);

# 退出当前进程（the calling process），并返回父进程定义的status
#include <stdlib.h>
void exit(int status);

# status Running Stopped Terminated 

# 创建进程，除了pid，同样的Copy (包括PC)
int pid = fork(); 
# call once, return twice，对于创建进程和子进程不同，子进程返回的pid即为0（自身）
int main() {
	pid_t pid;
	int x = 1;
    # 作为区分进程的参数，一份代码即可
    pid = Fork();
	if (pid == 0) { /* Child */
		printf("child : x=%d\n", ++x);
		exit(0);
	}

 	/* Parent */
	printf("parent: x=%d\n", --x);
	exit(0);
}
# 输出child 2, parent 0

# terminated后系统不会回收该进程，成为僵尸进程，直到被父进程Reaped回收。
# 内核为所有父进程terminated但未Reaped的进程提供了init进程，PID为1。

# waidpid，与子进程的交互，同时代表reaped
# pid = -1 所有子进程，*statusp &status，可以判断是正常退出WIFEXITED，WIFSIGNALED，由于发送的信号终止，Returns true if the child process terminated because of a signal that was not caught （offending signal)，WIFSTOPPED，由于子进程停止引起的handler。
pid_t waitpid(pid_t pid, int *statusp, int options);
# Returns: PID of child if OK, 0 (if WNOHANG), or −1 on error

# if WNOHANG was specified and one or more child(ren) specified by pid exist, but have not yet changed state, then 0 is returned
```

## 同步异步

Main函数 与 Handler函数，类似于多重中断处理的过程，需要考虑两者运行的先后顺序以及发生中断的时间。由于没有PV的信号量机制，Handler A B的先后顺序需要在A运行前屏蔽B的信号。

由于A的结束为导致B不再运行，还需要借助sigsuspend(&mask) (暂时开中断，直到中断结束) 确保所有子进程都被处理。

1. handler最好暂时保存全局变量errno，防止影响main函数的判断。
2. async-signal-safe function 不会被打断的函数，一般指可以通过单个微指令 (?) 完成的指令，参考CPU对系统调用的中断处理。
3. 处理全局变量前block all
4. volatile int g 不读reg（单进程的编译器可能优化，不再访存），借助声明可以强制访存，用于同步。
5. sig_atomic_t 原子操作赋值，可以不用block，注意不能flag++，同时读和写。

# 具体流程

```c
void eval(char *cmdline) {
    char *argv[MAXARGS]; /* Argument list execve() */
    char buf[MAXLINE]; /* Holds modified command line */
    int bg; /* Should the job run in bg or fg? */
    int jid;
    pid_t pid; /* Process id */
    sigset_t mask_all, mask_one, prev_one;
    sigfillset(&mask_all);
    sigemptyset(&mask_one);
    sigaddset(&mask_one, SIGCHLD);

    strcpy(buf, cmdline);
    bg = parseline(buf, argv);
    if (argv[0] == NULL)
        return; /* Ignore empty lines */

    if (!builtin_cmd(argv)) {
        // 同步 先add 后 delete 
        
        // 需要在handler可能出现之前先block
        sigprocmask(SIG_BLOCK, &mask_one, &prev_one);
        if ((pid = fork()) == 0) { 
            
            // 需要确保group与当前shell不同
            setpgid(0, 0);
            
            // 子进程开block，不影响execve的运行
            sigprocmask(SIG_SETMASK, &prev_one, NULL);  
            
            if (execve(argv[0], argv, environ) < 0) {
                printf("%s: Command not found.\n", argv[0]);
                // 注意exit()
                exit(0);
            }
        }

 
        if (!bg) {
            // 对全局变量进行写操作，block all 可以确保不会被其他的handler影响。
            sigprocmask(SIG_BLOCK, &mask_all, NULL);
            addjob(jobs, pid, FG, cmdline);
            // add完可以开block
            sigprocmask(SIG_SETMASK, &prev_one, NULL);
            waitfg(pid);
        }
        else {
            sigprocmask(SIG_BLOCK, &mask_all, NULL);
            addjob(jobs, pid, BG, cmdline);
            sigprocmask(SIG_SETMASK, &prev_one, NULL);
            jid = pid2jid(pid);
            printf("[%d] (%d) %s", jid, pid, cmdline);
        }
    }
    return;
}
```

```c
int builtin_cmd(char **argv) {
    if (!strcmp(argv[0], "quit")) /* quit command */
        exit(0);
    if (!strcmp(argv[0], "jobs")){
        listjobs(jobs);    
        return 1;
    } 
    if ((!strcmp(argv[0], "fg")) || (!strcmp(argv[0], "bg"))){
        do_bgfg(argv); 
        return 1;
    }
    if (!strcmp(argv[0], "&"))
        return 1;
    return 0; /* Not a builtin command */
}

```

```c
void do_bgfg(char **argv) {
    int pid, jid;
    struct job_t *cj;
    if (argv[1] == NULL) {
        printf("%s command requires PID or %%jobid argument\n", argv[0]);
        return;
    }
    if (argv[1][0] == '%') {
        jid = atoi(argv[1] + 1);
        cj = getjobjid(jobs, jid); 
        if (cj == NULL) {
            printf("%s: No such job\n", argv[1]);
            return; 
        }
        pid = cj->pid;
    }
    else if (isdigit(argv[1][0])){
        pid = atoi(argv[1]);
        cj = getjobpid(jobs, pid);
        if (cj == NULL) {
            printf("(%d): No such process\n", pid);
            return;
        }
        jid = cj->jid;
    }
    else {
        printf("%s: argument must be a PID or %%jobid\n", argv[0]);
        return;
    }
    
    if (argv[0][0] == 'b') {
        printf("[%d] (%d) %s", jid, pid, cj->cmdline);
        // 注意负数，kill所有同组的进程。
        kill(-pid, SIGCONT);
        cj->state = BG;
    }            
    else {
        kill(-pid, SIGCONT); 
        cj->state = FG;
        waitfg(pid);
    }
    return;
}
```

```c
// 建议waitpid只出现在一个函数中
// while (fgpid(jobs)>0)
//	sigsuspend(&masktemp);
// 注意这里有问题，需要先block子进程，否则若在while判断完成，进入sigsuspend前handler已经处理过了，就会导致一直等待。
// 这里也体现出同异步的问题很容易被忽略。

void waitfg(pid_t pid) {
    int status;
    sigset_t mask_all, prev_all;
    sigfillset(&mask_all);
    struct job_t *cj = getjobpid(jobs, pid);
    int jid = cj->jid;
    if (waitpid(pid, &status, WUNTRACED) > 0){
        if (WIFEXITED(status) || WIFSIGNALED(status)) {
            sigprocmask(SIG_BLOCK, &mask_all, &prev_all);
            deletejob(jobs, cj->pid);
            sigprocmask(SIG_SETMASK, &prev_all, NULL);
        }
        if (WIFSIGNALED(status)) {
            printf("Job [%d] (%d) terminated by signal %d\n", jid, pid, WTERMSIG(status));
        }
        else if (WIFSTOPPED(status)) {
            printf("Job [%d] (%d) stopped by signal %d\n", jid, pid, WSTOPSIG(status));
        }
    }
    else {
        unix_error("waitfg: waitpid error");
    }
    return;
}
```

```c
void sigchld_handler(int sig) {
    // 回收
    int olderrno = errno;
    sigset_t mask_all, prev_all;
    sigfillset(&mask_all);
    int pid, status;

    while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
        sigprocmask(SIG_BLOCK, &mask_all, &prev_all); 
        deletejob(jobs, pid);
        sigprocmask(SIG_SETMASK, &prev_all, NULL);
    }
    // if (errno != ECHILD) {
    //     unix_error("waitpid error");
    // }
    errno = olderrno;
    return;
}
```

```c
void sigint_handler(int sig) {
    int pid = fgpid(jobs);
    if (pid == 0) {
        return;
    }    
    else {
        kill(-pid, SIGINT);
    }
}

void sigtstp_handler(int sig) {
    int pid = fgpid(jobs);
    if (pid == 0) {
        return;
    }    
    else {
        struct job_t *cj = getjobpid(jobs, pid);
        cj->state = ST;  
        kill(-pid, SIGTSTP);
    }
}
```

