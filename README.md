# Speedtest-Graph
A set of tools for speedtest monitoring

![431188716_323631124035739_2731150893223690591_n](https://github.com/Kmac907/Speedtest-Graph/assets/120307903/48f191ad-844e-42a8-a7e3-87881c4529cf)

Workflow
- bash script creates a csv file and appends the results to it at a chosen interval
- graph script pulls the data from the csv and creates graphs viewable from a web browser with automatic updates at a chosen interval

Bash Script
- checks to see if a csv file already exists. If not it creates one
- pulls a list of all network interfaces configured, excluding the loopback interface
- uses ookla speedtest cli command to run a speedtest on the first interface listed
- formats the data into an easily readable format and appends the results to the csv found or created
- loops through each interface
- can be automated using tools like cronjob

Graph Script
- uses pandas, ploty and dash to create a graph using a csv file
- creates line graphs for download upload and latency. As well as an average of each stored in a table
- updates the webpage checking for new information every minute automatically
