gruntmet@ga-b3 src % leaks -atExit -- ./../build/graph
3*(x-2)))))
FAIL
Process:         graph [18665]
Path:            /Volumes/VOLUME/*/graph
Load Address:    0x10e109000
Identifier:      graph
Version:         ???
Code Type:       X86-64
Platform:        macOS
Parent Process:  leaks [18664]

Date/Time:       2023-03-19 22:12:31.336 +0300
Launch Time:     2023-03-19 22:12:21.211 +0300
OS Version:      macOS 11.6.6 (20G624)
Report Version:  7
Analysis Tool:   /Applications/Xcode.app/Contents/Developer/usr/bin/leaks
Analysis Tool Version:  Xcode 13.2.1 (13C100)

Physical footprint:         344K
Physical footprint (peak):  344K
----

leaks Report Version: 4.0
Process 18665: 173 nodes malloced for 16 KB
Process 18665: 3 leaks for 48 total leaked bytes.

    3 (48 bytes) << TOTAL >>
      1 (16 bytes) ROOT LEAK: 0x7fd5e5405f50 [16]  length: 1  ")"
      1 (16 bytes) ROOT LEAK: 0x7fd5e5405f60 [16]  length: 1  ")"
      1 (16 bytes) ROOT LEAK: 0x7fd5e5405f70 [16]  length: 1  ")"
