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

git clone git@github.com:cglacet/bear.git
cd bear
python insert_in_links.py
# rm -rf bear # Looks dangerous, TODO: find a better way 
