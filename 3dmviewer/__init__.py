import argparse

stl1 = """exception 1:
#include <stdio.h>
#include <winsock2.h>

int main() {
    WSADATA wsa;
    SOCKET server, client;
    struct sockaddr_in server_addr, client_addr;
    int client_len;
    char message[1024];

    WSAStartup(MAKEWORD(2,2), &wsa); // Init Winsock

    server = socket(AF_INET, SOCK_STREAM, 0); // TCP Socket

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(8080);

    bind(server, (struct sockaddr*)&server_addr, sizeof(server_addr)); // Bind to port
    listen(server, 3); // Start listening

    printf("Server waiting...\n");
    client_len = sizeof(client_addr);
    client = accept(server, (struct sockaddr*)&client_addr, &client_len); // Accept client

    recv(client, message, sizeof(message), 0); // Receive msg
    printf("Client says: %s\n", message);

    send(client, "Hello from server", strlen("Hello from server") + 1, 0); // Send response

    closesocket(server);
    WSACleanup();
    return 0;
}

#include <stdio.h>
#include <winsock2.h>

int main() {
    WSADATA wsa;
    SOCKET server, client;
    struct sockaddr_in server_addr, client_addr;
    int client_len;
    char message[1024];

    WSAStartup(MAKEWORD(2,2), &wsa); // Init Winsock

    server = socket(AF_INET, SOCK_STREAM, 0); // TCP Socket

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(8080);

    bind(server, (struct sockaddr*)&server_addr, sizeof(server_addr)); // Bind to port
    listen(server, 3); // Start listening

    printf("Server waiting...\n");
    client_len = sizeof(client_addr);
    client = accept(server, (struct sockaddr*)&client_addr, &client_len); // Accept client

    recv(client, message, sizeof(message), 0); // Receive msg
    printf("Client says: %s\n", message);

    send(client, "Hello from server", strlen("Hello from server") + 1, 0); // Send response

    closesocket(server);
    WSACleanup();
    return 0;
}


"""

stl2 = """exception 2:


#include<windows.h>
#include<stdio.h>
#define PIPE_NAME "\\\\.\\pipe\\MyPipe"
void main(){
    char buffer[1024];
    HANDLE pipe;
    DWORD byteRead,byteWrite;
    pipe = CreateNamedPipeA(
        PIPE_NAME, PIPE_ACCESS_DUPLEX,PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
        1,1024,1024,0,NULL);
    printf("Waiting for Client to connect..");
    ConnectNamedPipe(pipe,NULL);
    printf("\nClient Connected..\n");
    while(1){
        ReadFile(pipe,buffer,sizeof(buffer),&byteRead,NULL);
        buffer[byteRead] = '\0';
        if(!strcmp(buffer,"exit")){
            printf("Disconnected!!\n");
            break;
        }
        printf("Client: %s\n",buffer);
        printf("Server message to Client: ");
        fgets(buffer,sizeof(buffer),stdin);
        buffer[strcspn(buffer,"\n")] = '\0';
        WriteFile(pipe, buffer,strlen(buffer)+1,&byteWrite,NULL);
    }
    CloseHandle(pipe);
}


#include<windows.h>
#include<stdio.h>
#define PIPE_NAME "\\\\.\\pipe\\MyPipe"
void main(){
    HANDLE pipe;
    char buffer[1024];
    DWORD byteRead,byteWrite;
    pipe = CreateFileA(PIPE_NAME,GENERIC_READ | GENERIC_WRITE, 0 ,NULL, OPEN_EXISTING, 0,NULL);
    printf("Server Connected..\n");
    while (1){
        printf("Client: ");
        fgets(buffer,sizeof(buffer),stdin);
        buffer[strcspn(buffer,"\n")] = '\0';
        WriteFile(pipe,buffer,strlen(buffer)+1,&byteWrite,NULL);
        if(!strcmp(buffer,"exit")){
            printf("Disconnected!..");
            break;
        }
        ReadFile(pipe,buffer,sizeof(buffer),&byteRead,NULL);
        buffer[byteRead] = '\0';
        printf("From Server: %s\n",buffer);
    }
    CloseHandle(pipe);
}
"""

stl3 = """exception 3:
#include<stdio.h>
#include<stdlib.h>
#include<omp.h>

typedef struct matrix{
    int row;
    int col;
    int **array;
}matrix;
void print_mat(matrix* mat){
    for(int i=0;i<mat->row;i++){
        for(int j=0;j<mat->col;j++){
            printf("%d ",mat->array[i][j]);
        }
        printf("\n");
    }
}
matrix* matrix_mul(matrix* mat1,matrix* mat2){
    matrix* mat3 = (matrix*)malloc(sizeof(matrix));
    mat3->row = mat1->row;
    mat3->col = mat2->col;
    mat3->array = (int**)malloc(mat3->row*sizeof(int*));

    omp_set_num_threads(4);
    #pragma omp parallel shared(mat1,mat2,mat3)
    {
        #pragma for schedule(dynamic)
        for(int i=0;i<mat3->row;i++){
            int tid = omp_get_thread_num();
            mat3->array[i] = (int*)malloc(mat3->col*sizeof(int));
            for(int j=0;j<mat3->col;j++){
                //printf("Thread ID %d is working on %d row of matrix 1 and %d column of matrix 2\n",tid, i, j);
                int temp = 0;
                for(int k=0;k<mat2->row;k++){
                    temp += mat1->array[i][k]*mat2->array[k][j];
                }
                mat3->array[i][j] = temp;
            }
        }
    }
    return mat3;
}


void main(){
    srand(0); 
    matrix *mat1 = (matrix*)malloc(sizeof(matrix));
    matrix *mat2 = (matrix*)malloc(sizeof(matrix));
    printf("Size of matrix1: ");
    scanf("%d %d",&mat1->row,&mat1->col);
    printf("Size of matrix2: ");
    scanf("%d %d",&mat2->row,&mat2->col);
    mat1->array = (int**)malloc(mat1->row*sizeof(int *));
    mat2->array = (int**)malloc(mat2->row*sizeof(int *));
    for(int i=0;i<mat1->row;i++){
        mat1->array[i] = (int*)malloc(mat1->col*sizeof(int));
        for(int j=0;j<mat1->col;j++){
            mat1->array[i][j] = (rand()%10) + 1;
        }
    }
    for(int i=0;i<mat2->row;i++){
        mat2->array[i] = (int*)malloc(mat2->col*sizeof(int));
        for(int j=0;j<mat2->col;j++){
            mat2->array[i][j] = (rand()%10) + 1;
        }
    }
    printf("Matrix1: \n"); print_mat(mat1);
    printf("Matrix2: \n"); print_mat(mat2); 
    double t1 = omp_get_wtime();
    matrix* mat3 = matrix_mul(mat1,mat2);
    double t2 = omp_get_wtime();
    printf("mat1*mat2== \n"); print_mat(mat3);
    printf("\nFor parallel-tasking : %lf\n",t2-t1);
}
//ubuntu...
//gcc -fopenmp matrix_mul.c -o a -lpthread
//./a.out
"""

stl4 = """exception 4:
#include<mpi.h>
#include<stdio.h>
#include<stdlib.h>

int isduplicate(int *arr,int size,int id){
    for(int i=0;i<size;i++) if(arr[i]==id) return 1;
    return 0;
}

void main(int args,char **argv){
    int rank,size;
    MPI_Init(&args,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    srand(0);
    int req_per_worker = 1000/(size-1);
    int received_req[req_per_worker];
    if(rank == 0){
        int req[1000];
        for(int i=0;i<1000;i++) req[i] = rand()%100000;
        MPI_Scatter(req,req_per_worker,MPI_INT,received_req,req_per_worker,MPI_INT,0,MPI_COMM_WORLD);
    }else{
        MPI_Scatter(NULL,0,MPI_INT,received_req,req_per_worker,MPI_INT,0,MPI_COMM_WORLD);
        //check duplicates:
        int processed_id[req_per_worker];
        int count=0;
        for(int i=0;i<req_per_worker;i++){
            int id = received_req[i];
            if(!isduplicate(processed_id,count,id)){
                processed_id[count++] = id;
                printf("Worker %d - Serviced the req. %d\n",rank,id);
            }
        }
        MPI_Gather(&count,1,MPI_INT,NULL,1,MPI_INT,0,MPI_COMM_WORLD);
    }
    MPI_Finalize();
}

//mpicc Request.c
//mpirun -np 4 ./a.out
"""

stl5 = """exception 5:
This is placeholder for stl5
Line 2 of stl5...
"""

stl6 = """exception 6:
import java.util.*;

public class SimpleLamportEvent {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        int[] clock = new int[n]; // Initialize all clocks to 0

        while (true) {
            System.out.print("\nEnter sender process (or -1 to stop): ");
            int sender = sc.nextInt();
            if (sender == -1) break;

            System.out.print("Enter receiver process: ");
            int receiver = sc.nextInt();

            if (sender < 0 || sender >= n || receiver < 0 || receiver >= n) {
                System.out.println("Invalid process numbers. Try again.");
                continue;
            }

            // Sender increments clock before sending
            clock[sender]++;

            // Receiver updates clock using Lamport rule
            clock[receiver] = Math.max(clock[receiver], clock[sender]) + 1;

            System.out.println("\nEvent Summary:");
            System.out.println("P" + sender + " sent message at clock: " + clock[sender]);
            System.out.println("P" + receiver + " received and updated clock to: " + clock[receiver]);

            // Print clock status of all processes
            System.out.println("\nCurrent Clock Status of All Processes:");
            for (int i = 0; i < n; i++) {
                System.out.println("P" + i + ": " + clock[i]);
            }
        }

        System.out.println("\nSimulation Ended.");
        sc.close();
    }
}


import java.util.*;

public class SimpleVectorClock {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        int[][] vc = new int[n][n]; // vector clock for each process

        while (true) {
            System.out.print("\nEnter sender process (-1 to stop): ");
            int sender = sc.nextInt();
            if (sender == -1) break;

            System.out.print("Enter receiver process: ");
            int receiver = sc.nextInt();

            // 1. Sender increments its own clock
            vc[sender][sender]++;

            // 2. Send sender's vector to receiver
            for (int i = 0; i < n; i++) {
                vc[receiver][i] = Math.max(vc[receiver][i], vc[sender][i]);
            }

            // 3. Receiver increments its own clock
            vc[receiver][receiver]++;

            // 4. Show current status
            System.out.println("\nVector Clocks:");
            for (int i = 0; i < n; i++) {
                System.out.print("P" + i + ": ");
                for (int j = 0; j < n; j++) {
                    System.out.print(vc[i][j] + " ");
                }
                System.out.println();
            }
        }

        System.out.println("\nSimulation Done.");
        sc.close();
    }
}
"""

stl7 = """exception 7:
import java.util.*;

public class RicartAgrawala {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of processes: ");
        int total = sc.nextInt();

        int[] requestTime = new int[total]; // stores latest request timestamp for each process

        while (true) {
            System.out.print("\nEnter process requesting CS (-1 to stop): ");
            int process = sc.nextInt();
            if (process == -1) break;

            if (process < 0 || process >= total) {
                System.out.println("Invalid process number!");
                continue;
            }

            System.out.print("Enter timestamp of request: ");
            int time = sc.nextInt();
            requestTime[process] = time;

            int replyCount = 0;

            // Check each other process to see if it replies
            for (int i = 0; i < total; i++) {
                if (i != process) {
                    int otherTime = requestTime[i];
                    if (otherTime == 0 || time < otherTime || (time == otherTime && process < i)) {
                        replyCount++;
                        System.out.println("Process " + i + " replies to " + process);
                    } else {
                        System.out.println("Process " + i + " delays reply to " + process);
                    }
                }
            }

            if (replyCount == total - 1) {
                System.out.println("==> Process " + process + " ENTERS the Critical Section.");
            } else {
                System.out.println("==> Process " + process + " is WAITING for replies.");
            }
        }

        System.out.println("\nSimulation Ended.");
        sc.close();
    }
}
"""

stl8 = """exception 8:
import java.util.*;

public class SuzukiKasami {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Step 1: Get number of processes
        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        int[] RN = new int[n]; // Request Numbers
        int[] LN = new int[n]; // Last Executed
        Arrays.fill(RN, 0);
        Arrays.fill(LN, 0);

        while (true) {
            // Step 2: Get process request
            System.out.print("\nEnter process requesting CS (-1 to stop): ");
            int req = sc.nextInt();

            if (req == -1) break;

            if (req < 0 || req >= n) {
                System.out.println("Invalid process number! Try again.");
                continue;
            }

            // Step 3: Update RN
            RN[req]++;

            // Show state
            System.out.println("RN: " + Arrays.toString(RN));
            System.out.println("LN: " + Arrays.toString(LN));

            // Step 4: Check eligibility
            System.out.println("\nChecking token eligibility:");
            for (int i = 0; i < n; i++) {
                if (RN[i] > LN[i]) {
                    System.out.println("Process " + i + " gets the TOKEN.");
                    LN[i] = RN[i]; // Update after entering CS
                } else {
                    System.out.println("Process " + i + " does NOT get the token.");
                }
            }

            System.out.println("Updated LN: " + Arrays.toString(LN));
        }

        System.out.println("\nSimulation ended.");
        sc.close();
    }
}
"""

stl9 = """exception 9:
import java.util.Scanner;

public class MitchellMerrettDeadlockDetection {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Step 1: Get the number of processes
        System.out.print("Enter number of processes: ");
        int n = sc.nextInt();

        // Step 2: Initialize label array for processes (0 initially)
        int[] labels = new int[n];  // Label for each process
        for (int i = 0; i < n; i++) {
            labels[i] = 0;  // Initially, label is 0
        }

        // Step 3: Get the resources allocation and requests
        int[] request = new int[n]; // Array to track process requests
        int[] hold = new int[n];    // Array to track process holding resources

        for (int i = 0; i < n; i++) {
            System.out.print("Process " + i + " (Enter 1 if holding resource, 0 if not): ");
            hold[i] = sc.nextInt();
            System.out.print("Process " + i + " (Enter 1 if requesting resource, 0 if not): ");
            request[i] = sc.nextInt();
        }

        // Step 4: Detect deadlock using Mitchell-Merrett's algorithm

        boolean deadlockDetected = false;
        while (!deadlockDetected) {
            // Step 4.1: Look for a process that is holding and requesting resources
            boolean found = false;
            for (int i = 0; i < n; i++) {
                if (hold[i] == 1 && request[i] == 1) {
                    // Increment the label for the process
                    labels[i]++;
                    found = true;
                    System.out.println("Process " + i + " incremented its label to: " + labels[i]);

                    // Check if the incremented label indicates a deadlock (circular wait)
                    for (int j = 0; j < n; j++) {
                        if (request[j] == 1 && labels[j] == labels[i]) {
                            System.out.println("Deadlock detected between Process " + i + " and Process " + j);
                            deadlockDetected = true;
                            break;
                        }
                    }

                    // If deadlock not detected, break the loop and check for next request
                    if (!deadlockDetected) {
                        break;
                    }
                }
            }

            // Step 4.2: If no deadlock and no process was found, break
            if (!found) {
                System.out.println("No deadlock detected.");
                break;
            }
        }

        sc.close();
    }
}
"""

stl10 = """exception 10:
________________________________________
✅ Step-by-step Guide to Run the Hadoop WordCount Program on WSL (Ubuntu)
🔧 1. Install Java
Hadoop needs Java to run. In your Ubuntu terminal:
bash
CopyEdit
sudo apt update
sudo apt install openjdk-11-jdk -y
java -version
________________________________________
📦 2. Download and Set Up Hadoop
bash
CopyEdit
cd ~
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
mv hadoop-3.3.6 hadoop
Set environment variables:
bash
CopyEdit
nano ~/.bashrc
Add these lines at the end:
bash
CopyEdit
export HADOOP_HOME=~/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
Save and close the file. Then run:
bash
CopyEdit
source ~/.bashrc
Check if Hadoop works:
bash
CopyEdit
hadoop version
________________________________________
📝 3. Create WordCount.java File
Inside your home folder:
bash
CopyEdit
mkdir ~/wordcount
cd ~/wordcount
nano WordCount.java
Paste your program and save with CTRL+O, Enter, CTRL+X.

import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
public class WordCount {

    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            context.write(key, new IntWritable(sum));
        }
    }
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

________________________________________
🛠️ 4. Compile the Program
bash
CopyEdit
mkdir classes
javac -classpath "$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/mapreduce/*" -d classes WordCount.java
jar -cvf wordcount.jar -C classes/ .
________________________________________
📁 5. Prepare Input and Output Directories
Create input file:
bash
CopyEdit
mkdir input
echo "hello hadoop hadoop world" > input/test.txt
________________________________________
🚀 6. Run Hadoop in Local (Standalone) Mode
Run your program locally (no need for HDFS):
bash
CopyEdit
hadoop jar wordcount.jar WordCount input output
If output folder already exists, delete it: rm -r output
________________________________________
📂 7. Check Output
bash
CopyEdit
cat output/part-r-00000
You should see something like:
txt
CopyEdit
hadoop  2
hello   1
world   1
________________________________________
🧠 Tech Stack Explanation
Tool	Purpose
Java	Programming language for Hadoop jobs
Hadoop	Big data framework for MapReduce computation
MapReduce	Model for distributed computation (Mapper + Reducer)
Ubuntu WSL	Linux environment inside Windows


"""

stl11 = """exception 11:

"""

stl12 = """exception 12:
This is placeholder for stl12
Line 2 of stl12...
"""

# ... You can add stl4 to stl12 here

exceptions = {
    'stl1': stl1,
    'stl2': stl2,
    'stl3': stl3,
    'stl4': stl4,
    'stl5': stl5,
    'stl6': stl6,
    'stl7': stl7,
    'stl8': stl8,
    'stl9': stl9,
    'stl10': stl10,
    'stl11': stl11,
    'stl12': stl12,
}


def main():
    parser = argparse.ArgumentParser(description="Show exception content by name")
    parser.add_argument('stlname', type=str, help='exception name like stl1, stl2...')
    args = parser.parse_args()

    stl_content = exceptions.get(args.stlname.lower())
    if stl_content:
        print(stl_content)
    else:
        print("Oops! Invalid exception name. Try one of:", ', '.join(exceptions.keys()))

if __name__ == "__main__":
    main()
