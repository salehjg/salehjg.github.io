---
layout: post
title:  "How to build OpenCV from source for Android"
date:   2023-03-7 12:32:45 +0330
categories:
---
# How to build OpenCV from source for Android
<img align="right" width="150" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/800px-OpenCV_Logo_with_text_svg_version.svg.png">
Recently, I had to use OpenCV in an Android Studio project and unfortenately the off-the-shelf, ready to use binaries on the internet were not quite compatible with my setup.
So it took me a couple of days to workout the issues and I thought it might be helpful to document the process for later use by me or someone else.

# Pre Requisities
1. Use a Linux OS. It is assumed that `Arch Linux` is used.
2. Install the latest version of `Android Studio`.
3. Use `SDK Manger` of `Android Studio` to install your `SDK 25`, `NDK 21.4.7075529`, and `BuildTools 25.0.3` of your choice.
4. Install the packages that we are going to need on your linux: `sudo pacman -S cmake git aria2 ant unzip`

# OpenCV Versions
If you need the `cv1` interface of OpenCV, you should use version<4. Versions>=4 only have the `cv2` interface.
We are going to use OpenCV 3.4.16 .

# Android SDK Tools
The `android` executable of Android SDK located at `sdk/tools/android` which is used by OpenCV's CMake scripts to setup the java module project is depricated by Google. Unfortunately, OpenCV, even the latest versions of it, still use this depricated executable. The workaround is to download an older version of this file from Google and use it instead. 
(as described [here](https://forum.unity.com/threads/solved-android-command-deprecated-error-unable-to-list-target-platforms.458814/))

## Downgrading `Sdk/tools`
```
$ cd ~/Downloads
$ aria2 -x8 http://dl-ssl.google.com/android/repository/tools_r25.2.5-linux.zip
$ mv ~/Android/Sdk/tools ~/Android/Sdk/tools.ORIG
$ unzip tools_r25.2.5-linux.zip -d ~/Android/Sdk/
``` 

# Get OpenCV Source 
```
$ cd ~
$ mkdir opencv_repo
$ cd opencv_repo
$ aria2 -x8 https://github.com/opencv/opencv/archive/refs/tags/3.4.16.zip
$ aria2 -x8 https://github.com/opencv/opencv_contrib/archive/refs/tags/3.4.16.zip
$ unzip opencv-3.4.16.zip
$ unzip opencv_contrib-3.4.16.zip
$ cd opencv-3.4.16
$ aria2 https://gist.githubusercontent.com/salehjg/2ce2ef90071eaa3ba7f3404f4094ae12/raw/41f1533729283affb1c02c00af4fd81e9d57aa2b/cmake_conf.sh
```
Now open `cmake_conf.sh` and edit the path lines. Save it and continue.
```
$ mkdir 00_build
$ mkdir 01_ndk_outputs
$ cd 00_build
$ bash ../cmake_conf.sh
$ make all -j8
$ make install
```
The NDK version of OpenCV should be available in `01_ndk_outputs` now.

# Android SDK Tools
Now that we are finished with the old `android` executable, we have to restore the original version of the `sdk/tools` directory.

## Resoring the original `Sdk/tools`
```
$ rm -rf ~/Android/Sdk/tools ~/Android/Sdk/
$ mv ~/Android/Sdk/tools.ORIG ~/Android/Sdk/tools
``` 

# Setting up the Android Studio project
1. Follow [this gist to build OpenCV shared library for Android](https://gist.github.com/salehjg/2ce2ef90071eaa3ba7f3404f4094ae12#file-opencv-ndk-build-md).
2. Create a new project, Java, MinSDK API26.
3. In `Project Side Bar`, right click on `App` and select `New -> Folder -> JNI Folder`.
4. Check the `Change Folder Location` check box and rename the last part of the path from `src/main/jni/` to `src/main/jniLibs/` .
5. Go to your `OpenCV/01_ndk_outputs/sdk/native/libs` source directory and select all the folders and copy them into `jniLibs` of your Android Studio project.
6. It is assumed that your phone is a `arm64-v8a`.
7. Open your app's `build.gradle` and add this to `defaultConfig` entry:
```
externalNativeBuild{
            cmake{
                cppFlags "-frtti -fexceptions"
                abiFilters 'arm64-v8a'
            }
        }
```
8. Also, make sure that app's `build.gradle`, the `android` entry has this member (you can skip steps 3 and 4, create `jniLibs` manualy and copy this into `build.gradle`):
```
sourceSets {
        main {
            jni {
                srcDirs 'src/main/jni', 'src/main/jniLibs'
            }
        }
    }
```
9. Copy `opencv/01_ndk_outputs/sdk` into the base directory of your Android Studio project and then rename the `sdk` into `opencv`.
10. Inside the `opencv` directory, open `build.gradle` with a code editor.
11. Edit `compileSdkVersion`, `targetSdkVersion`, and `minSdkVersion` to match your Android Studio project.
12. Edit `JavaVersion` and change it to `VERSION_1_8`, otherwise your app will crash on startup.
13. In Android Studio, change the `Project Side Bar` mode from `Android` to `Project`.
14. Find the `opencv` directory and open `local.properties` and make sure the `sdk.dir` is set correctly.
15. Find and open `settings.gradle` in the `Project Side Bar` on `Project` mode and append `include ':opencv'` to it and `Sync` the gradle script.
16. Find and open app's `build.gradle` and add `implementation project(path: ':opencv')` to the `dependencies` entry and `Sync` the gradle script.
17. Open `activity_main.xml` and copy this:
```
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    xmlns:opencv="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent" >

    <org.opencv.android.JavaCameraView
        android:layout_width="fill_parent"
        android:layout_height="fill_parent"
        android:visibility="gone"
        android:id="@+id/HelloOpenCvView"
        opencv:show_fps="true"
        opencv:camera_id="any" />

</LinearLayout>
```
18. Open `AndroidManifest.xml` and add these outside the `application` entry:
```
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" />
    <uses-feature android:name="android.hardware.camera.autofocus" />
    <uses-feature android:name="android.hardware.camera.front" />
    <uses-feature android:name="android.hardware.camera.front.autofocus" />
```
19. Open `MainActivity.java` and replace the content with:
```

public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {
    private CameraBridgeViewBase mOpenCvCameraView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        System.loadLibrary("opencv_java3");
        Mat a = new Mat(100,200, CvType.CV_8UC1);
        Mat b = new Mat(100,200, CvType.CV_8UC1);

        getPermissions();

        mOpenCvCameraView = (CameraBridgeViewBase) findViewById(R.id.HelloOpenCvView);
        mOpenCvCameraView.setVisibility(SurfaceView.VISIBLE);
        mOpenCvCameraView.setCvCameraViewListener(this);

    }

    private void getPermissions() {
        String[] requiredPermission = {
                android.Manifest.permission.CAMERA,
        };
        ActivityCompat.requestPermissions(MainActivity.this, requiredPermission, 100);
    }

    @Override
    public void onRequestPermissionsResult (int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults){
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == 100) {

            boolean allPermission = true;
            for (int i = 0; i < grantResults.length-2; i++) {
                if (grantResults[i] != PackageManager.PERMISSION_GRANTED) {
                    allPermission = false;
                }
            }
            if (allPermission) {
                Toast.makeText(this, "Perms granted.", Toast.LENGTH_SHORT).show();
                mOpenCvCameraView.enableView();
            } else {
                Toast.makeText(this, "Failed to get the perms.", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    public void onCameraViewStarted(int width, int height) {

    }

    @Override
    public void onCameraViewStopped() {

    }

    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {
        Mat src = inputFrame.rgba();

        Mat gray = new Mat(src.rows(), src.cols(), src.type());
        Mat edges = new Mat(src.rows(), src.cols(), src.type());

        org.opencv.imgproc.Imgproc.cvtColor(src, gray, org.opencv.imgproc.Imgproc.COLOR_RGB2GRAY);
        org.opencv.imgproc.Imgproc.Canny(gray, edges, 100, 100*3);
        return edges;
    }

    @Override
    public void onPause() {
        super.onPause();
        if (mOpenCvCameraView != null)
            mOpenCvCameraView.disableView();
    }

    public void onDestroy() {
        super.onDestroy();
        if (mOpenCvCameraView != null)
            mOpenCvCameraView.disableView();
    }
}
```
20. Build the project.
21. Connect your phone and run the app on the device.
22. On the device (mine is API26) accept the permissions.
23. Now you should be able to see the live camera feed with `Canny` algorithm applied.

 
