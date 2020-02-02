from libs.Downloader import Downloader

Downloader = Downloader("test", '1.12.2')

print("[1/8] test fetch_manifest()")
Downloader.fetch_manifest()
print("[2/8] test fetch_data_list()")
Downloader.fetch_data_list()
print("[3/8] test read_details()")
Downloader.read_details()
print("[4/8] test fetch_client_file()")
Downloader.fetch_client_file()
print("[5/8] test fetch_all_libs()")
Downloader.fetch_all_libs()
print("[6/8] test fetch_all_libs_natives()")
Downloader.fetch_all_libs_natives()
print("[7/8] test fetch_all_res()")
Downloader.fetch_all_res()
print("[8/8] test fetch_all_res()")
Downloader.extract_natives()

print("[POST STEP] COMPLIE MINECRAFT")
Downloader.complie_minecraft()
print("OK")
