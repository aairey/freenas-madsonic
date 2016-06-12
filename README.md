# freenas-madsonic
Madsonic 5.1 plugin for FreeNAS 9.10.
It's v5.1 and not v6.x because there is no port out yet for FreeBSD.
## Installing
Use the `.pbi` file in the `/pkg` directory.
Import it in the FreeNAS GUI under Plugins.
## Compiling
Instructions for a clean FreeBSD 10 image:
```
freebsd-update fetch install
pkg install git gcc subversion
freebsd-update fetch install
portsnap fetch update
portsnap extract
pushd /usr/ports/devel/xdg-utils
make && make install
#below steps might not be necessary
#echo "media:*:816:816::0:0:Media Plugins Daemon:/nonexistent:/usr/sbin/nologin" >> /usr/ports/UIDs
#echo "media:*:816:" >> /usr/ports/GIDs
# to get pbi_makeport on FreeBSSD, install the sources from this repo
git clone https://github.com/josh4trunks/freenas-plugins
pushd freenas-plugins/src/
pushd libsh/
make && make install
popd
pushd pbi-wrapper
make && make install
popd
mv pbi_wrapper/.pbi-wrapper-amd64 pbi-manager/
pushd pbi-manager
make && make install
popd
pushd pbi-manager10
make && make install
popd
popd
# clone this repo, create a pbi from the port on this system
git clone https://github.com/aairey/freenas-madsonic
cd freenas-madsonic
pbi_makeport -c ./plugins/madsonic -o ./pbi --pkgdir ./pkg www/madsonic-standalone

```
## Known Issues
Currently not able to build!
Getting this as output:
```
Running buildworld / installworld (into a chroot)
Copying FreeBSD sources to chroot environment
Creating chroot environment...
tar: could not chdir to '/usr/pbi/.pbi-world-amd64'

cp: /usr/pbi/madsonic-amd64.chroot.935/etc/resolv.conf: No such file or directory
cp: /usr/pbi/madsonic-amd64.chroot.935/usr/local/sbin is not a directory
cp: /usr/pbi/madsonic-amd64.chroot.935/usr/local/sbin/pbi_makeport: No such file or directory
chmod: /usr/pbi/madsonic-amd64.chroot.935/usr/local/sbin/pbi_*: No such file or directory
Copying /root/freenas-madsonic/plugins/madsonic -> /usr/pbi/madsonic-amd64.chroot.935/pbimodule
chroot: /usr/local/sbin/pbi_makeport_chroot: No such file or directory
Cleaning /usr/pbi/madsonic-amd64.chroot.935

```

## Contributing
Pull Requests welcome!

## Credits
https://github.com/josh4trunks/freenas-plugins - for the pbi_makeport sources
https://github.com/MadMarty/FreeNAS-Plugins - for the work on Subsonic FreeNas plugin
