if ! command -v git 2>&1 >/dev/null; then 
    if ! command -v brew 2>&1 >/dev/null; then 
        echo "Installing homebrew (https://brew.sh/)"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
        echo "Installing Git"
        brew install git
    fi
fi

if ! command -v python 2>&1 >/dev/null; then 
    echo "Installing Python"
    brew install python
fi

TMP_DIR=$(mktemp -d)

echo "Retreiving source from Github (https://github.com/cglacet)."
git clone -q git@github.com:cglacet/bear.git $TMP_DIR
if [ $? -eq 0 ]; then 
    echo "Running python script: "
    python ${TMP_DIR}/insert_in_links.py | sed 's/^/    /'
else
    echo "Failed to retreive code from Github"
fi
rm -rf $TMP_DIR
