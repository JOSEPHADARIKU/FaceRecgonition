from detector.video_stream import VideoStream

def main():
    vs = VideoStream(source=0)
    vs.start()

if __name__ == "__main__":
    main()