/**
 * COMMAND TO COMPILE THIS FILE :
 * g++ -o open_cv_test open_cv_test.cpp -I/path/to/opencv/include `pkg-config --libs opencv`


 * 
*/

#include <iostream>
#include <opencv2/opencv.hpp>
#include <unistd.h> // for usleep function

int main() {
    // Image Capture Test
    cv::VideoCapture camera(0); // Use camera index 0

    if (!camera.isOpened()) {
        std::cerr << "Error: Could not open camera." << std::endl;
        return 1;
    }

    cv::Mat frame;
    if (!camera.read(frame)) {
        std::cerr << "Error: Could not read frame." << std::endl;
        return 1;
    }

    cv::imwrite("captured_image.jpg", frame);

    camera.release();

    std::cout << "Image captured successfully!" << std::endl;

    // Camera Recording Test
    cv::VideoCapture videoCamera(0);

    if (!videoCamera.isOpened()) {
        std::cerr << "Error: Could not open camera." << std::endl;
        return 1;
    }

    int width = static_cast<int>(videoCamera.get(cv::CAP_PROP_FRAME_WIDTH));
    int height = static_cast<int>(videoCamera.get(cv::CAP_PROP_FRAME_HEIGHT));
    int fps = 30;

    cv::VideoWriter videoWriter("recorded_video.avi", cv::VideoWriter::fourcc('X', 'V', 'I', 'D'), fps, cv::Size(width, height));

    if (!videoWriter.isOpened()) {
        std::cerr << "Error: Could not create VideoWriter." << std::endl;
        return 1;
    }

    int durationInSeconds = 5;
    int frameCount = 0;

    while (frameCount < durationInSeconds * fps) {
        cv::Mat frame;
        if (!videoCamera.read(frame)) {
            std::cerr << "Error: Could not read frame." << std::endl;
            break;
        }

        videoWriter.write(frame);
        frameCount++;
    }

    videoCamera.release();
    videoWriter.release();

    std::cout << "Video recorded successfully!" << std::endl;

    // Camera Stream Test
    cv::VideoCapture streamCamera("/dev/video2");

    if (!streamCamera.isOpened()) {
        std::cerr << "Error: Could not open camera." << std::endl;
        return 1;
    }

    cv::namedWindow("Camera Stream", cv::WINDOW_NORMAL);

    int streamDurationInSeconds = 5;
    int streamFrameCount = 0;

    while (streamFrameCount < streamDurationInSeconds * fps) {
        cv::Mat frame;
        if (!streamCamera.read(frame)) {
            std::cerr << "Error: Could not read frame." << std::endl;
            break;
        }

        cv::imshow("Camera Stream", frame);

        if (cv::waitKey(1) == 'q') {
            break;
        }

        streamFrameCount++;
    }

    streamCamera.release();
    cv::destroyAllWindows();

    std::cout << "Camera stream finished." << std::endl;

    return 0;
}
