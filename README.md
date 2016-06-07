# freenas-madsonic
Madsonic 6.0 plugin for FreeNAS 9.3
## Installing
Use the `.pbi` file in the `/pkg` directory.
Import it in the FreeNAS GUI under Plugins.
## Compiling
Instructions for a clean FreeBSD 10 image:
```
pkg install git
freebsd-update fetch install
portsnap fetch update
#below steps might not be necessary
#echo "media:*:816:816::0:0:Media Plugins Daemon:/nonexistent:/usr/sbin/nologin" >> /usr/ports/UIDs
#echo "media:*:816:" >> /usr/ports/GIDs
git clone https://github.com/aairey/freenas-madsonic
cd freenas-madsonic
pbi_makeport -c ./plugins/madsonic -o ./pbi --pkgdir ./pkg/madsonic

```
## Contributing
Pull Requests welcome!

## Credits
https://github.com/MadMarty/FreeNAS-Plugins
