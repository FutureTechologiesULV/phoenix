import serial

# Function to interpret 24-bit data as a signed 32-bit integer
def interpret24bitAsInt32(byte_array):
    new_int = (
        ((0xFF & byte_array[0]) << 16) |
        ((0xFF & byte_array[1]) << 8)  |
        (0xFF & byte_array[2])
    )
    if (new_int & 0x00800000) > 0:  # Check if the sign bit (23rd bit) is set
        new_int |= 0xFF000000  # If negative, set the upper 8 bits to 1s to form a negative 32-bit value
    else:
        new_int &= 0x00FFFFFF  # Keep only the lower 24 bits for positive numbers
    return new_int

# Function to convert raw counts to microvolts
def convert_to_microvolts(raw_value, gain=24):
    scale_factor = 4.5 / (gain * (2**23 - 1))  # Scale factor in volts per count
    return raw_value * scale_factor * 1e6  # Convert to microvolts

# Initialize the serial connection (update COM port accordingly)
ser = serial.Serial(port='COM4', baudrate=115200)  # Replace 'COMx' with your port name

def start_streaming():
    ser.write(b'b')  # Send start streaming command

def stop_streaming():
    ser.write(b's')  # Send stop streaming command

def read_data():
    while True:
        if ser.in_waiting:
            packet = ser.read(33)  # Read 33 bytes of data
            if packet[0] == 0xA0:  # Check for the header
                eeg_data = []
                for i in range(8):
                    eeg_channel_data = packet[3 + i * 3 : 6 + i * 3]  # Extract 3 bytes for each channel
                    eeg_value = interpret24bitAsInt32(eeg_channel_data)  # Interpret the 24-bit value
                    eeg_in_microvolts = convert_to_microvolts(eeg_value)  # Convert to microvolts
                    eeg_data.append(eeg_in_microvolts)
                print("EEG Data in microvolts: ", eeg_data)

# Start the streaming
start_streaming()

try:
    read_data()
except KeyboardInterrupt:
    stop_streaming()
    ser.close()
