This project builds ART Java runtime from Android for Mac OS X in Xcode.

### Goals ###

1. Create Mac OS X setup for playing with ART / Jack & Jill
  * I would love to experiment with adding new features (like value types) without having to think of how to get them through javac
2. Create embeddable JVM for Mac OS X / iOS
  * Runtime for the "extended Java" language above
  * RoboVM alternative

The reality however, is that none of those goals are achieved, and the most you can do right now is to run simple apps (like HelloWorld).

### Getting started ###

##### Prerequisites #####

1. Mac OS X 10.9+
2. Xcode 6+
3. Android SDK with KitKat (API 19) tools

##### Building #####

1. Clone the repo
2. Run `./gyp_generate.py --android-sdk-root <path to the Android SDK>`
3. Open `projects/xcode/ARTPart.xcworkspace`
4. Build `out` target (32-bit)

##### Running #####

* Run `testapps-HelloWorld` target (32-bit)
* Build and run arbitrary Java files with `run_java.py` (e.g. `./run_java.py --sources platform/art/test/302-float-conversion --main-class-name Main`)
