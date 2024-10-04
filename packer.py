import requests
import shutil
import os

# GitHub API URLs
HATH_RUST_RELEASES_URL = "https://api.github.com/repos/james58899/hath-rust/releases/latest"
HATH_RUST_PACKER_URL = "https://api.github.com/repos/AsenHu/hath-rust_Packer/releases/latest"

def get_latest_tag(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['tag_name']

def get_packer_latest_tag(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['tag_name']
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            return "v0.0.0"
        else:
            raise err

def download_file(url, file_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_name, 'wb') as file:
        file.write(response.content)

def main():
    # 获取最新标签
    hath_rust_latest = get_latest_tag(HATH_RUST_RELEASES_URL)
    hath_rust_packer_latest = get_packer_latest_tag(HATH_RUST_PACKER_URL)

    print(f"Latest hath-rust version: {hath_rust_latest}")
    print(f"Latest hath-rust_Packer version: {hath_rust_packer_latest}")

    # 检查更新
    if hath_rust_latest == hath_rust_packer_latest:
        print("No updates available.")
        return

    # 下载文件
    print("Downloading hath-rust binaries...")
    download_file(f"https://github.com/james58899/hath-rust/releases/download/{hath_rust_latest}/hath-rust-x86_64-unknown-linux-gnu", "hath-gnu")
    download_file(f"https://github.com/james58899/hath-rust/releases/download/{hath_rust_latest}/hath-rust-x86_64-unknown-linux-musl", "hath-musl")

    # 准备工作
    os.makedirs('deb/usr/bin', exist_ok=True)
    os.system('chmod +x ./hath-gnu')
    os.system('chmod +x ./hath-musl')
    with open('deb/DEBIAN/control', 'a') as file:
        file.write(f'Version: {hath_rust_latest.lstrip('v')}\n')

    # 打包成 deb
    # gnu
    print("Packaging into .deb files...")
    shutil.move('hath-gnu', 'deb/usr/bin/hath')
    os.system('dpkg-deb -Zxz -Sextreme -z9 -vD -b ./deb hath-gnu.deb')
    # musl
    shutil.rmtree('deb/usr/bin/hath', ignore_errors=True)
    shutil.move('hath-musl', 'deb/usr/bin/hath')
    os.system('dpkg-deb -Zxz -Sextreme -z9 -vD -b ./deb hath-musl.deb')

if __name__ == "__main__":
    main()