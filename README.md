# Universal APK decompiler 
This tool is just a python tool that allow you to decompile an apk with multiple tools to avoid getting only certain part of the code by using one specific decompiler
it automaticaly download decompiler, convert to jar for java specific tools

### decompiler taken in charge :
 - apktool
 - jadx
 - fernflower
 - procyon
 - crf
 - androguad
 - baksmali
 
### dex to jar : enjarify

output path : ./apk_out
input path : ./apk.apk

### TODO :
 - add arguments settings
  - make state between decompiler (Same size ? file diff (git diff) ?)
  https://github.com/AlexeySoshin/smali2java
  https://github.com/Storyyeller/Krakatau
  https://bytecodeviewer.com/