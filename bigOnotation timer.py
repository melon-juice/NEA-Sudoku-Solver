Dim timer As New Stopwatch()
timer.Start()
For x = 1 to 1000000000
   #count to one billion!
Next
timer.Stop()
# Get the elapsed time as a TimeSpan value. 
Dim el As TimeSpan = stopWatch.Elapsed

# Format and display the TimeSpan value. 
Dim formattedTime As String = String.Format("{0}:{1}:{2}.{3}", el.Hours, el.Minutes, el.Seconds, el.Milliseconds / 10)
Console.WriteLine( "Time Elapsed: " + formattedTime)
