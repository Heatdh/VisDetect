gst-launch-1.0 nvarguscamerasrc ! nvoverlaysink

gst-launch-1.0 nvarguscamerasrc sensor_mode=0 ! 'video/x-raw(memory:NVMM),width=3820, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=616' ! nvvidconv ! nvegltransform ! nveglglessink -e

ssh -L 5000:localhost:5000 eaglevisions@eaglevisions-desktop.local

nmcli c
nmcli d connect wlan0

Xvfb :1 -screen 0 1920x1080x24+32 -fbdir /var/tmp &
export DISPLAY=:1

