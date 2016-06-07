import hashlib
import json
import os
import pwd
import urllib

from django.utils.translation import ugettext_lazy as _

from dojango import forms
from madsonicUI.freenas import models, utils

class MadsonicForm(forms.ModelForm):

    class Meta:
        model = models.Madsonic
        widgets = {
            'madsonic_max_memory': forms.widgets.TextInput(),
            'madsonic_port': forms.widgets.TextInput(),
            'madsonic_ssl_password': forms.widgets.PasswordInput(),
        }
        exclude = ('enable',)

    def __init__(self, *args, **kwargs):
        self.jail_path = kwargs.pop('jail_path')
        super(MadsonicForm, self).__init__(*args, **kwargs)

        self.fields['madsonic_ssl_keystore'].widget = forms.widgets.TextInput(attrs={
            'data-dojo-type': 'freeadmin.form.PathSelector',
            'root': self.jail_path,
            'dirsonly': 'false',
            })

    def clean_subsonic_ssl_password(self):
        subsonic_ssl_password = self.cleaned_data.get("madsonic_ssl_password")
        if not madsonic_ssl_password:
            return self.instance.madsonic_ssl_password
        return madsonic_ssl_password

    def save(self, *args, **kwargs):
        obj = super(MadsonicForm, self).save(*args, **kwargs)

        rcconf = os.path.join(utils.madsonic_etc_path, "rc.conf")
        with open(rcconf, "w") as f:
            if obj.enable:
                f.write('madsonic_enable="YES"\n')

        settingsfile = os.path.join(utils.madsonic_etc_path, "madsonic.conf")
        settings = {}

        for field in obj._meta.local_fields:
            if field.attname not in utils.madsonic_settings:
                continue
            info = utils.madsonic_settings.get(field.attname)
            value = getattr(obj, field.attname)
            _filter = info.get("filter")
            if _filter:
                settings[info.get("field")] = _filter(value)
            else:
                settings[info.get("field")] = value

        madsonic_ssl = str(obj.madsonic_ssl).lower()
        with open(settingsfile, 'w') as f:
            f.write('MADSONIC_MAX_MEMORY="%d"\n' % (obj.madsonic_max_memory, ))
            f.write('MADSONIC_SSL="%s"\n' % (madsonic_ssl, ))
            f.write('MADSONIC_SSL_KEYSTORE="%s"\n' % (obj.madsonic_ssl_keystore, ))
            f.write('MADSONIC_SSL_PASSWORD="%s"\n' % (obj.madsonic_ssl_password, ))
            f.write('MADSONIC_PORT="%d"\n' % (obj.madsonic_port, ))
            f.write('MADSONIC_CONTEXT_PATH="%s"\n' % (obj.madsonic_context_path, ))
            f.write('MADSONIC_LOCALE="%s"' % (obj.madsonic_locale, ))

        os.system(os.path.join(utils.madsonic_pbi_path, "tweak-rcconf"))
