import urllib.request
import os
import json

class Downloader():
    urls = {"manifest": "https://launchermeta.mojang.com/mc/game/version_manifest.json", "res_download": "http://resources.download.minecraft.net/%s/%s"}
    files = {}
    directories = ["D", ".minecraft/assets/indexes", ".minecraft/assets/objects", ".minecraft/libraries", ".minecraft/versions"]

    def _Is_this_exist(self, file_or_folder):
        return os.path.exists(file_or_folder)

    def _mkpath(self, name):
        return os.path.join(self.dir, name)

    def __init__(self, Directory, Target, Platfrom = 'linux'):
        self.dir = Directory
        self.target = Target
        self.natives = 'natives-%s' % Platfrom

        self.check_and_create(Directory)
        for s in self.directories:
            d_name = self._mkpath(s)
            self.check_and_create(d_name)
            pass

        self.files.update({'manifest': self._mkpath("D/version_manifest.json")})
        self.files.update({'target': self._mkpath("D/target.json")})
        self.files.update({'res': self._mkpath(os.path.join(".minecraft/assets/indexes", self.target + ".json"))})
        pass

    def check_and_create(self, d):
        if (not self._Is_this_exist(d)):
            os.system("mkdir -p %s" % d)
            pass
        pass

    def _move(self, a, b):
        os.system("mv %s %s" % (a, b))
        pass

    def _copy(self, a, b):
        os.system("cp -rf %s %s" % (a, b))
        pass

    def read_details(self):
        with open(self.files['target'], 'r') as f:
            self.Details = json.load(f)
            pass
        pass

    def _Download_data(self, URL, save_as):
        download_command_format = "wget -q --show-progress -O %s %s"

        while (True):
            status = os.system(download_command_format % (save_as, URL))

            if (status == 0):
                break
            pass
        pass
    
    def fetch_file(self, f_name, url):
        if (self._Is_this_exist(f_name)):
            print("File %s, Skip" % f_name)
            pass
        else:
            self._Download_data(url, f_name)
            pass
        pass

    def fetch_manifest(self):
        self.fetch_file(self.files['manifest'], self.urls['manifest'])
        pass

    def fetch_data_list(self):
        with open(self.files["manifest"], "r") as f:
            mainifest = json.load(f)
            pass

        for a in mainifest['versions']:
            if (a['id'] == self.target):
                target_details = a
                break
            pass

        self.fetch_file(self.files['target'], target_details['url'])
        pass

    def fetch_client_file(self):
        versions_dir = self._mkpath('.minecraft/versions/%s' % self.target)
        self.check_and_create(versions_dir)

        self.fetch_file(os.path.join(versions_dir, self.target + ".jar"), self.Details['downloads']['client']['url'])
    pass

    def fetch_all_libs(self):
        for d in self.Details['libraries']:
            if ("artifact" in d['downloads']):
                file_path = self._mkpath(os.path.join('.minecraft/libraries', d['downloads']['artifact']['path']))
                self.check_and_create(os.path.dirname(file_path))

                self.fetch_file(file_path, d['downloads']['artifact']['url'])
                pass
            pass
        pass

    def fetch_all_libs_natives(self):
        for d in self.Details['libraries']:
            if ("classifiers" in d['downloads'] and self.natives in d['downloads']['classifiers']):
                file_path = self._mkpath(os.path.join('.minecraft/libraries', d['downloads']['classifiers'][self.natives]['path']))
                self.check_and_create(os.path.dirname(file_path))

                self.fetch_file(file_path, d['downloads']['classifiers'][self.natives]['url'])
                pass
            pass
        pass

    def fetch_all_res(self):
        self.fetch_file(self.files['res'], self.Details['assetIndex']['url'])
        objects_d = self._mkpath('.minecraft/assets/objects')

        with open(self.files['res'], 'r') as f:
            Details = json.load(f)
            pass

        for d in Details['objects'].values():
            header = os.path.join(objects_d, d['hash'][0:2])
            self.check_and_create(header)
            self.fetch_file(os.path.join(header, d['hash']), self.urls['res_download'] % (d['hash'][0:2], d['hash']))
            pass
        pass

    def extract_natives(self):
        natives = (os.popen("find %s | grep %s" % (self.dir, self.natives))).readlines()

        for i in range(len(natives)):
            natives[i] = natives[i].replace('\n', '')
            os.system("unzip -n %s -d %s" % (natives[i], os.path.join(self._mkpath('.minecraft/versions/%s' % self.target), self.target+'-natives')))
            pass
        pass
    
    def complie_minecraft(self):
        self._copy(self.files['target'], self._mkpath('.minecraft/versions/%s/%s.json' % (self.target, self.target)))
        pass

    def clean(self):
        os.system("rm -rf %s" % self._mkpath('D'))
        pass
    pass
