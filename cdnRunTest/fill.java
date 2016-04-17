
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.Socket;
import java.util.Date;

public class CDNClient {

	public static final String path = "./Test_SD_H264.ts.001";
	public static final String addr = "192.168.24.133";
	public static final int port = 8100;// 8100
	public static final int TIMEOUT = 0;
	public static final int BUFFER_SIZE = 32 * 1024 * 1024;

	public void send() {
		System.out.println("CDNClient:: send---------------");
		Socket socket = null;

		// byte[] recvBuf = new byte[BUFFER_SIZE];
		//byte[] sendBuf = new byte[BUFFER_SIZE];

		Date start = new Date();
		System.out.println("start at:" + start.getTime());

		// client从文件读取数据到内存中
		// TODO
		byte[] sendBuf = readDataByBytes(path);
                if(sendBuf == null){
                    return;
                }
		// sendBuf = new String("hello world! zhengyw test!").getBytes();
		System.out.println("sendBuf.length = " + sendBuf.length);
		System.out.println("sendBuf is :\n" + (new String(sendBuf)).length());

		// socket发送数据
		try {
			socket = new Socket(addr, port);
			socket.setSoTimeout(TIMEOUT);

			socket.getOutputStream().write(sendBuf, 0, sendBuf.length);
			socket.getOutputStream().flush();
			Thread.sleep(10);
			socket.close();

		} catch (IOException e) {
			System.out.println("Error: IOException error");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Error: Exception error");
			e.printStackTrace();
		} finally {
			try {
				if (socket != null) {
					socket.close();
				}
			} catch (IOException e) {
				System.out.println("Error:  finally IOException error");
				e.printStackTrace();
			}
		}

		Date end = new Date();
		System.out.println("start at:" + end.getTime());
		System.out.println("time _spend:" + (end.getTime() - start.getTime()));
	}

	/**
	 * 以行为单位读取文件，常用于读面向行的格式化文件
	 * 
	 * @param path
	 * @return
	 */
	public static byte[] readDataByLines(String path) {
		System.out.println("以行为单位读取文件内容");
		System.out.println("path is :" + path);
		
		byte[] buffer = new byte[BUFFER_SIZE];
		int line = 0;
		String str = "";
		String temp = "";

		BufferedReader br = null;
		try {
			br = new BufferedReader(new FileReader(path));

			while ((temp = br.readLine()) != null) {
				str += temp;
				line++;
			}
			System.out.println("line = " + line);
			System.out.println("str is :" + str);

			br.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		}
		try {
			buffer = str.getBytes("GBK");
		} catch (UnsupportedEncodingException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		return buffer;
	}

	/**
	 * 以字节为单位读取文件，常用于读二进制文件，如图片、声音、影像等文件
	 * 
	 * @param path
	 * @return
	 */
	public static byte[] readDataByBytes(String path) {
		System.out.println("以字节为单位读取文件内容");
		System.out.println("path is :" + path);

		byte[] buffer = new byte[BUFFER_SIZE];
		
		int offset = 0;
		int recvlen = 0;

		File file = new File(path);
		InputStream in = null;
		try {
			in = new FileInputStream(file);
			while ((recvlen = in.read(buffer, offset, BUFFER_SIZE - offset)) > 0) {
				offset += recvlen;
			}
			System.out.println("buffer len is :" + offset);
                        byte[] bufferRet = new byte[offset];
                        System.arraycopy(buffer, 0, bufferRet, 0, offset);
			//System.out.write(buffer);
			System.out.println();
			in.close();

                        return bufferRet;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			if (in != null) {
				try {
					in.close();
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		}
		return null;

	}

	/**
	 * 以字符为单位读取文件，常用于读文本，数字等类型的文件
	 * 
	 * @param path
	 * @return
	 */
	public static char[] readDataByChars(String path) {
		System.out.println("以字符为单位读取文件内容");
		System.out.println("path is :" + path);

		char[] buffer = new char[BUFFER_SIZE];
		
		int offset = 0;
		int recvlen = 0;

		File file = new File(path);
		InputStreamReader in = null;
		try {
			in = new InputStreamReader(new FileInputStream(file));
			while ((recvlen = in.read(buffer, offset, BUFFER_SIZE - offset)) > 0) {
				offset += recvlen;
			}
			//System.out.println("buffer is :"+buffer.toString());

			in.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			if (in != null) {
				try {
					in.close();
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
		}
		return buffer;

	}

	public static void main(String args[]) throws UnsupportedEncodingException {
		System.out.println("-------------------------------------- start ");
		
		byte[] bufbyte = new byte[BUFFER_SIZE];
		bufbyte = CDNClient.readDataByBytes(CDNClient.path);
		System.out.println("bufbyte ::::::::::::::::::::::::::::::::: start");
		//System.out.println("bufbyte is: " + new String(bufbyte, "GBK"));
		try {
			//System.out.write(bufbyte);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println();
		System.out.println("bufbyte ::::::::::::::::::::::::::::::::: end ");
		
		
		CDNClient cdn = new CDNClient();
		cdn.send();
		System.out.println("end --------------------------------------");

	}
}

