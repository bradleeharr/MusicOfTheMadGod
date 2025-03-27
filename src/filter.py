import time
import pyaudio

def main():
    FORMAT = pyaudio.paInt16   # 16-bit int sampling
    CHANNELS = 1               # Stereo
    RATE = 44100               # 44.1 kHz sample rate
    FRAMES_PER_BUFFER = 32   # Buffer size

    p = pyaudio.PyAudio()

    cable_input_candidates = []
    cable_output_candidates = []
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        
        d_name = dev['name'].lower()
        # Only include devices with "VB-Audio." Exclude "16ch" and "Point"
        if "vb-audio" not in d_name or "16ch" in d_name or "point" in d_name:
            continue
        if "input" in d_name:
            cable_input_candidates.append((i, dev))
        if "output" in d_name:
            cable_output_candidates.append((i, dev))

    print("========== Output Candidates ==========")
    [print(dev) for idx, dev in cable_output_candidates]

    input_stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          input_device_index=cable_output_candidates[0][0], # TODO: Clarify that this will work always 
                          frames_per_buffer=FRAMES_PER_BUFFER)

    output_stream = p.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           output=True,
                           #output_device_index=3,
                           frames_per_buffer=FRAMES_PER_BUFFER)

    print("Audio passthrough is running. Press Ctrl+C to exit.")

    try:
        start_time = time.time()
        mute = 0
        while True:
            
            if (time.time() - start_time) > 5: 
                mute = not mute
                start_time = time.time()



            data = input_stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)

            # (Optional) Process the audio data here before outputting

            output_stream.write(data)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        input_stream.stop_stream()
        input_stream.close()
        output_stream.stop_stream()
        output_stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
