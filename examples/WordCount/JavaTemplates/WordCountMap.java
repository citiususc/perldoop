import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

	public class WordCountMap extends Mapper<Object, Text,Text , Text>{
		
		@Override
		public void map(Object incomingKey, Text value, Context context) throws IOException, InterruptedException {
			try{
			
			//<java><start>

			//<java><end>
			
			}
			catch(Exception e){
				System.out.println(e.toString());
			}
		}
	}
