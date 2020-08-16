﻿using System;
using System.IO;
using System.Diagnostics;

namespace PythonSample
{
    class Program
    {
        static void Main(string[] args)
        {

            var cmd = "C:/Users/Abhipray/source/repos/PythonSample/untitled0.py";
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python37_64/python.exe",
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
            Console.Read();
        }

        static void Process_OutputDataReceived(object sender, DataReceivedEventArgs e)
        {
            Console.WriteLine(e.Data);
        }

    }
}

