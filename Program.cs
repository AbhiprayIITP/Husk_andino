using System;
using System.IO;
using System.Diagnostics;

namespace PythonSample
{
    class Program
    {
        static void Main(string[] args)
        {

            var cmd = "Oled3.py";
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "/usr/bin/python",
                    Arguments = cmd,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                },
                EnableRaisingEvents = true
            };
            process.ErrorDataReceived += Process_OutputDataReceived;
            process.OutputDataReceived += Process_OutputDataReceived;

            process.Start();
            process.BeginErrorReadLine();
            process.BeginOutputReadLine();
            process.WaitForExit();
            Console.WriteLine("Program Over");
            Console.Read();
        }

        static void Process_OutputDataReceived(object sender, DataReceivedEventArgs e)
        {
            //Console.WriteLine(e.Data);
            string[] FileList = e.Data?.Split(' ');
            string Temp = String.Empty;
            string Gsm = String.Empty;
            string RS232 = String.Empty;
            string RS485 = String.Empty;
            string Ethernet = String.Empty;
            if(FileList != null){
            //foreach (string x in FileList)
            //Console.WriteLine(x);
            Temp = FileList[0];
            Gsm = FileList[1];
            RS232 = FileList[2];
            RS485 = FileList[3];
            Ethernet = FileList[4];
            }
           Console.WriteLine("{0} {1} {2} {3} {4}",Temp,Gsm,RS232,RS485,Ethernet);
        }

    }
}

