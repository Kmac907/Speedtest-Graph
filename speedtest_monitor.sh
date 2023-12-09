#!/bin/bash

# Check if the CSV file exists, if not, create it with headers
if [ ! -f speedtest_results.csv ]; then
    echo "Timestamp,Interface,Server,ISP,Download,Upload,Latency" > speedtest_results.csv
fi

# Get a list of all network interfaces excluding 'lo'
interfaces=($(ip -o link show | awk -F': ' '$2 != "lo" {print $2}'))

# Function to run speed test for a specific interface and append results to CSV
run_speed_test() {
    interface=$1
    echo "Running speed test for $interface..."

    # Run speedtest with the correct options and output format
    result=$(speedtest --interface $interface --format=json | tail -n 1)

    # Check if the speed test was successful and does not contain the error message
    if [ $? -eq 0 ] && ! echo "$result" | grep -q "error"; then
        # Extract download and upload speeds directly from bytes field
        download_bytes=$(echo "$result" | jq -r '.download.bytes')
        upload_bytes=$(echo "$result" | jq -r '.upload.bytes')

        # Check if download and upload bytes are greater than 0
        if (( $download_bytes > 0 )) && (( $upload_bytes > 0 )); then
            # Convert bytes to megabits (1 byte = 8 bits)
            download=$(echo "$download_bytes / 1250000" | bc -l)
            upload=$(echo "$upload_bytes / 1250000" | bc -l)

            # Format the values with two decimal places
            download_formatted=$(printf "%.2f" $download)
            upload_formatted=$(printf "%.2f" $upload)

            # Get current timestamp
            timestamp=$(date +"%Y-%m-%d %T")

            # Extract server name and ISP from the result
            server_name=$(echo "$result" | jq -r '.server.name')
            isp=$(echo "$result" | jq -r '.isp')

            # Extract latency values
            latency_low=$(echo "$result" | jq -r '.ping.low')

            # Append results to CSV with timestamp
            echo "$timestamp,$interface,$server_name,$isp,$download_formatted,$upload_formatted,$latency_low" >> speedtest_results.csv

            echo "Speed test for $interface completed successfully."
        else
            echo "Speed test for $interface failed. Please check your internet connection."
        fi
    else
        echo "Speed test for $interface failed. Please check your internet connection."
    fi
}

# Loop through each interface and run speed test
for interface in "${interfaces[@]}"; do
    run_speed_test $interface
done
