[app]
title = Tung Sahour
package.name = tungsahour
package.domain = org.tung
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 1.0
requirements = python3,pygame
orientation = landscape
fullscreen = 1

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 0
