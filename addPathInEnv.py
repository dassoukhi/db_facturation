import subprocess


def addPathInEnv(name, path):
    try:
        path = path.replace(" ","$")
        print('setx CHROMEPATH ' + path)
        outputChrome = subprocess.check_output(
            'setx ' + name + ' ' + path,
            shell=True
        )
        print(f"Success adding path in ENV variable, please restart your machine for local path to be supported.")
    except Exception as err:
        print("Error failed :", err)

if __name__ == "__main__":
    addPathInEnv('HELLO','test')